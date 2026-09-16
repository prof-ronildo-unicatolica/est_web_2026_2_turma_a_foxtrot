from typing import List
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CidadeCreateSchema(BaseModel):
    nome: str


class CidadeResponseSchema(BaseModel):
    id: UUID
    nome: str

    model_config = ConfigDict(from_attributes=True)


class HotelCreateSchema(BaseModel):
    """O que o cliente envia em POST /hoteis.

    A cidade entra como ID, nao como objeto: assim nao ha duvida se e para
    reaproveitar uma cidade existente ou criar uma nova (e sempre reaproveitar).
    """

    nome: str = Field(min_length=1, max_length=100)
    cidade_id: UUID


class HotelResponseSchema(BaseModel):
    """O que a API devolve.

    A cidade vem ANINHADA e completa: sem isso o frontend precisaria de uma
    requisicao extra por hotel so para descobrir o nome da cidade.
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    nome: str
    cidade: CidadeResponseSchema


class CidadeComHoteisSchema(CidadeResponseSchema):
    """Cidade com a lista de hoteis dentro. Usada so onde ela for pedida
    explicitamente -- ver a nota sobre recursao infinita no item 4.
    """

    hoteis: List[HotelResponseSchema] = []
