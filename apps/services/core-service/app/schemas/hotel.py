from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CidadeCreateSchema(BaseModel):
    nome: str


class CidadeResponseSchema(BaseModel):
    id: UUID
    nome: str

    model_config = ConfigDict(from_attributes=True)