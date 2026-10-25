
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.core.rabbitmq import publish_event
from app.models.quarto import Quarto
from app.models.reserva import Reserva
from app.models.usuario import Usuario
from app.schemas.reserva import ReservaCreateSchema, ReservaResponseSchema
from app.services.reserva_service import calcular_total_reserva


router = APIRouter(prefix="/reservas", tags=["Reservas"])


@router.post(
    "",
    response_model=ReservaResponseSchema,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Solicita uma reserva",
)
async def criar_reserva(
    payload: ReservaCreateSchema,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    quarto = db.query(Quarto).filter(Quarto.id == payload.quarto_id).first()

    if quarto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quarto nao encontrado.",
        )

    if payload.quantidade_adultos > quarto.max_adultos:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Quantidade de adultos excede a capacidade do quarto.",
        )

    if payload.quantidade_criancas > quarto.max_criancas:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Quantidade de criancas excede a capacidade do quarto.",
        )

    total = calcular_total_reserva(
        preco_diaria=Decimal(str(quarto.preco_diaria)),
        data_checkin=payload.data_checkin,
        data_checkout=payload.data_checkout,
    )

    reserva = Reserva(
        usuario_id=usuario.id,
        quarto_id=quarto.id,
        data_checkin=payload.data_checkin,
        data_checkout=payload.data_checkout,
        quantidade_adultos=payload.quantidade_adultos,
        quantidade_criancas=payload.quantidade_criancas,
        quantidade_bebes=0,
        early_checkin=False,
        late_checkout=False,
        necessita_berco=False,
        tarifa_tipo="Flexivel",
        data_limite_cancelamento=None,
        valor_multa_cancelamento=Decimal("0.00"),
        valor_total=total,
        status="Pendente",
    )

    try:
        db.add(reserva)
        db.flush()
        db.commit()
        db.refresh(reserva)
    except Exception:
        db.rollback()
        raise

    try:
        await publish_event(
            "solicitacoes-reserva",
            {"reserva_id": str(reserva.id)},
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "Reserva criada como Pendente, mas nao foi possivel publicar "
                "a solicitacao no RabbitMQ."
            ),
        ) from exc

    return reserva
