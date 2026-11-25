
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db, get_mongo_db
from app.models.avaliacao import Avaliacao
from app.models.quarto import Quarto
from app.models.usuario import Usuario
from app.schemas.avaliacao import AvaliacaoCreate, AvaliacaoResponse
from app.services.avaliacao_service import validar_reserva_para_avaliacao
from app.services.catalogo_hotel_service import CatalogoHotelService


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
    reserva = validar_reserva_para_avaliacao(
        db=db,
        reserva_id=payload.reserva_id,
        usuario_id=usuario.id,
    )

    avaliacao_existente = (
        db.query(Avaliacao)
        .filter(Avaliacao.reserva_id == reserva.id)
        .first()
    )

    if avaliacao_existente is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Esta reserva ja possui uma avaliacao.",
        )

    quarto = (
        db.query(Quarto)
        .filter(Quarto.id == reserva.quarto_id)
        .first()
    )

    if quarto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quarto da reserva nao encontrado.",
        )

    avaliacao = Avaliacao(
        reserva_id=reserva.id,
        hotel_id=quarto.hotel_id,
        nota=payload.nota,
        comentario=payload.comentario,
    )

    try:
        db.add(avaliacao)
        db.commit()
        db.refresh(avaliacao)
    except Exception:
        db.rollback()
        raise

    await CatalogoHotelService(
        db,
        mongo_db,
    ).sincronizar_hotel(quarto.hotel_id)

    return avaliacao
