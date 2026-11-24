from datetime import date
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.reserva import Reserva


def validar_reserva_para_avaliacao(
    db: Session,
    reserva_id: UUID,
    usuario_id: UUID,
) -> Reserva:
    """Valida se uma reserva pode ser avaliada conforme a RFO12."""

    # 1. Busca a reserva pertencente ao usuario autenticado.
    reserva = (
        db.query(Reserva)
        .filter(
            Reserva.id == reserva_id,
            Reserva.usuario_id == usuario_id,
        )
        .first()
    )

    if reserva is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reserva nao encontrada.",
        )

    # 2. Apenas reservas confirmadas podem ser avaliadas.
    if reserva.status != "Confirmada":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Apenas reservas confirmadas podem ser avaliadas.",
        )

    # 3. O check-out deve estar no passado.
    if reserva.data_checkout >= date.today():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A reserva so pode ser avaliada apos o check-out.",
        )

    return reserva