from typing import Any
from uuid import UUID

from motor.motor_asyncio import AsyncIOMotorDatabase
from sqlalchemy.orm import Session

from app.repositories.catalogo_hotel_repository import CatalogoHotelRepository
from app.repositories.hotel_repository import HotelRepository


class HotelNaoEncontradoParaCatalogoError(Exception):
    pass


class CatalogoHotelService:
    """Monta e sincroniza a projeção de um hotel no MongoDB."""

    def __init__(
        self,
        db: Session,
        mongo_db: AsyncIOMotorDatabase,
    ):
        self.hoteis = HotelRepository(db)
        self.catalogo = CatalogoHotelRepository(mongo_db)

    async def sincronizar_hotel(self, hotel_id: UUID) -> None:
        hotel = self.hoteis.get_by_id(hotel_id)

        if not hotel:
            raise HotelNaoEncontradoParaCatalogoError(
                f"Nao existe hotel com id '{hotel_id}'."
            )

        documento = self._montar_documento(hotel)

        await self.catalogo.substituir_hotel(
            hotel_id=str(hotel.id),
            documento=documento,
        )

    async def buscar_por_filtros(
        self,
        cidade_id: UUID | None = None,
        categoria_estrelas: int | None = None,
    ) -> list[dict[str, Any]]:
        return await self.catalogo.buscar_por_filtros(
            cidade_id=str(cidade_id) if cidade_id else None,
            categoria_estrelas=categoria_estrelas,
        )

    @staticmethod
    def _montar_documento(hotel: Any) -> dict[str, Any]:
        return {
            "hotel_id": str(hotel.id),
            "nome": hotel.nome,
            "categoria_estrelas": hotel.categoria_estrelas,
            "cidade": {
                "id": str(hotel.cidade.id),
                "nome": hotel.cidade.nome,
                "limite_territorial": hotel.cidade.limite_territorial,
            },
            "comodidades": [
                {
                    "id": str(comodidade.id),
                    "nome": comodidade.nome,
                }
                for comodidade in hotel.comodidades
            ],
            "quartos": [
                {
                    "id": str(quarto.id),
                    "numero": quarto.numero,
                    "tipo": quarto.tipo,
                    "preco_diaria": float(quarto.preco_diaria),
                    "max_adultos": quarto.max_adultos,
                    "max_criancas": quarto.max_criancas,
                }
                for quarto in hotel.quartos
            ],
        }