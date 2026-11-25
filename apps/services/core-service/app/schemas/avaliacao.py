from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AvaliacaoCreate(BaseModel):
    reserva_id: UUID
    nota: int = Field(ge=1, le=5)
    comentario: str | None = None


class AvaliacaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    reserva_id: UUID
    hotel_id: UUID
    nota: int
    comentario: str | None
