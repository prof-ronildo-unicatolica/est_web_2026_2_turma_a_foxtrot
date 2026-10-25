from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ReservaCreateSchema(BaseModel):
    quarto_id: UUID
    data_checkin: date
    data_checkout: date
    quantidade_adultos: int = Field(ge=1)
    quantidade_criancas: int = Field(default=0, ge=0)


class ReservaResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    usuario_id: UUID
    quarto_id: UUID
    data_checkin: date
    data_checkout: date
    quantidade_adultos: int
    quantidade_criancas: int
    quantidade_bebes: int
    early_checkin: bool
    late_checkout: bool
    necessita_berco: bool
    tarifa_tipo: str
    data_limite_cancelamento: date | None
    valor_multa_cancelamento: Decimal
    valor_total: Decimal
    status: str