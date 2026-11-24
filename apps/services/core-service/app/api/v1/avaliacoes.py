from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.reserva import Reserva
from app.models.usuario import Usuario
from app.services.avaliacao_service import (
    validar_reserva_para_avaliacao,
)


router = APIRouter(
    prefix="/avaliacoes",
    tags=["Avaliacoes"],
)


def obter_reserva_elegivel(
    reserva_id: UUID,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
) -> Reserva:
    """Verifica se o usuario pode avaliar a reserva."""

    return validar_reserva_para_avaliacao(
        db=db,
        reserva_id=reserva_id,
        usuario_id=usuario.id,
    )