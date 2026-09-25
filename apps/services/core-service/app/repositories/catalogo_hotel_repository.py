from typing import Any

from motor.motor_asyncio import AsyncIOMotorDatabase


class CatalogoHotelRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["catalogo_hoteis"]

    async def substituir_hotel(
        self,
        hotel_id: str,
        documento: dict[str, Any],
    ) -> None:
        await self.collection.replace_one(
            {"hotel_id": hotel_id},
            documento,
            upsert=True,
        )

    async def buscar_por_id(
        self,
        hotel_id: str,
    ) -> dict[str, Any] | None:
        return await self.collection.find_one(
            {"hotel_id": hotel_id},
            {"_id": 0},
        )

    async def listar(self) -> list[dict[str, Any]]:
        cursor = self.collection.find(
            {},
            {"_id": 0},
        )
        return await cursor.to_list(length=None)

    async def buscar_por_filtros(
        self,
        cidade_id: str | None = None,
        categoria_estrelas: int | None = None,
    ) -> list[dict[str, Any]]:
        filtro: dict[str, Any] = {}

        if cidade_id is not None:
            filtro["cidade.id"] = cidade_id

        if categoria_estrelas is not None:
            filtro["categoria_estrelas"] = categoria_estrelas

        cursor = self.collection.find(
            filtro,
            {"_id": 0},
        )

        return await cursor.to_list(length=None)