
from typing import List
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CidadeCreateSchema(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    limite_territorial: dict | None = None


class CidadeResponseSchema(BaseModel):
    id: UUID
    nome: str
    limite_territorial: dict | None = None

    model_config = ConfigDict(from_attributes=True)


class HotelCreateSchema(BaseModel):
    """O que o cliente envia em POST /hoteis."""

    nome: str = Field(min_length=1, max_length=100)
    cidade_id: UUID
    categoria_estrelas: int = Field(ge=1, le=5)


class HotelResponseSchema(BaseModel):
    """O que a API devolve."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    nome: str
    categoria_estrelas: int
    cidade: CidadeResponseSchema
    media_avaliacoes: float = 0.0
    quantidade_avaliacoes: int = 0


class CidadeComHoteisSchema(CidadeResponseSchema):
    hoteis: List[HotelResponseSchema] = []


class ComodidadeCreateSchema(BaseModel):
    nome: str = Field(min_length=1, max_length=100)


class ComodidadeResponseSchema(BaseModel):
    id: UUID
    nome: str

    model_config = ConfigDict(from_attributes=True)


class QuartoCreateSchema(BaseModel):
    hotel_id: UUID
    numero: str = Field(min_length=1, max_length=10)
    tipo: str = Field(min_length=1, max_length=50)
    preco_diaria: float = Field(ge=0)
    max_adultos: int = Field(ge=1)
    max_criancas: int = Field(default=0, ge=0)


class QuartoResponseSchema(BaseModel):
    id: UUID
    hotel_id: UUID
    numero: str
    tipo: str
    preco_diaria: float
    max_adultos: int
    max_criancas: int

    model_config = ConfigDict(from_attributes=True)
