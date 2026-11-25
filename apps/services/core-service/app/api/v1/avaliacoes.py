import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db, get_mongo_db
from app.models.avaliacao import Avaliacao
from app.models.quarto import Quarto
from app.models.usuario import Usuario
from app.schemas.avaliacao import AvaliacaoCreate, AvaliacaoResponse
from app.services.avaliacao_service import validar_reserva_para_avaliacao
from app.services.catalogo_hotel_service import CatalogoHotelService

logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/avaliacoes",
    tags=["Avaliacoes"],
)


@router.post(
    "",
    response_model=AvaliacaoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cria uma avaliacao para uma reserva concluida",
)
async def criar_avaliacao(
    payload: AvaliacaoCreate,
    db: Session = Depends(get_db),
    mongo_db=Depends(get_mongo_db),
    usuario: Usuario = Depends(get_current_user),
):
    # Valida a reserva conforme a RFO12.
    reserva = validar_reserva_para_avaliacao(
        db=db,
        reserva_id=payload.reserva_id,
        usuario_id=usuario.id,
    )

    # Verifica se a reserva ja possui uma avaliacao.
    avaliacao_existente = (
        db.query(Avaliacao).filter(Avaliacao.reserva_id == reserva.id).first()
    )

    if avaliacao_existente is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Esta reserva ja possui uma avaliacao.",
        )

    # Identifica o quarto e o hotel da reserva.
    quarto = db.query(Quarto).filter(Quarto.id == reserva.quarto_id).first()

    if quarto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quarto da reserva nao encontrado.",
        )

    hotel_id = quarto.hotel_id

    # Cria a avaliacao.
    avaliacao = Avaliacao(
        reserva_id=reserva.id,
        hotel_id=hotel_id,
        nota=payload.nota,
        comentario=payload.comentario,
    )

    # Persiste a avaliacao no banco relacional.
    try:
        db.add(avaliacao)
        db.commit()

    except IntegrityError as exc:
        db.rollback()

        # Identifica a restricao de unicidade no PostgreSQL.
        diagnostico = getattr(exc.orig, "diag", None)
        restricao = getattr(diagnostico, "constraint_name", None)

        # Identifica a mesma restricao no SQLite dos testes.
        erro_sqlite = "UNIQUE constraint failed: avaliacoes.reserva_id" in str(exc.orig)

        if restricao == "uq_avaliacoes_reserva_id" or erro_sqlite:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Esta reserva ja possui uma avaliacao.",
            ) from exc

        # Outros erros de integridade nao sao duplicidades.
        raise

    except Exception:
        db.rollback()
        raise

    db.refresh(avaliacao)

    # Atualiza a media de avaliacoes no catalogo MongoDB.
    # Uma falha na sincronizacao nao invalida a avaliacao salva.
    try:
        await CatalogoHotelService(
            db,
            mongo_db,
        ).sincronizar_hotel(hotel_id)

    except Exception:
        logger.exception(
            "Falha ao sincronizar o catalogo do hotel %s "
            "apos registrar a avaliacao %s.",
            hotel_id,
            avaliacao.id,
        )

    return avaliacao
