
from datetime import date
from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ReservaCreate(BaseModel):
    quarto_id: UUID
    data_checkin: date
    data_checkout: date

    quantidade_adultos: int = Field(ge=1)
    idades_criancas: list[int] = Field(default_factory=list)

    early_checkin: bool = False
    late_checkout: bool = False
    necessita_berco: bool = False

    tarifa_tipo: Literal["flexivel", "nao_reembolsavel"] = "flexivel"

    servicos_adicionais_ids: list[UUID] = Field(default_factory=list)

    @model_validator(mode="after")
    def validar_reserva(self):
        if self.data_checkin < date.today():
            raise ValueError("O check-in não pode estar no passado.")

        if self.data_checkout <= self.data_checkin:
            raise ValueError(
                "O check-out deve ser posterior ao check-in."
            )

        if any(
            idade < 0 or idade > 12
            for idade in self.idades_criancas
        ):
            raise ValueError(
                "A idade das crianças deve estar entre 0 e 12 anos."
            )

        if len(set(self.servicos_adicionais_ids)) != len(
            self.servicos_adicionais_ids
        ):
            raise ValueError(
                "Existem serviços adicionais duplicados."
            )

        return self


class ReservaResponse(BaseModel):
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


class ReservaCriadaResponse(BaseModel):
    id: UUID
    status: str
    mensagem: str
