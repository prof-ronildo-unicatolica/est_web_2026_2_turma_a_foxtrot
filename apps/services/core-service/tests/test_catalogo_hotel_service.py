from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
from app.repositories.catalogo_hotel_repository import CatalogoHotelRepository

import asyncio

from app.services.catalogo_hotel_service import (
    CatalogoHotelService,
    HotelNaoEncontradoParaCatalogoError,
)


def test_sincronizar_hotel_substitui_documento_no_mongo():
    hotel_id = uuid4()
    cidade_id = uuid4()
    comodidade_id = uuid4()
    quarto_id = uuid4()

    hotel = SimpleNamespace(
        id=hotel_id,
        nome="Hotel Teste",
        categoria_estrelas=4,
        cidade=SimpleNamespace(
            id=cidade_id,
            nome="Limoeiro do Norte",
            limite_territorial=None,
        ),
        comodidades=[
            SimpleNamespace(id=comodidade_id, nome="Piscina")
        ],
        quartos=[
            SimpleNamespace(
                id=quarto_id,
                numero="101",
                tipo="Luxo",
                preco_diaria=Decimal("250.00"),
                max_adultos=2,
                max_criancas=1,
            )
        ],
    )

    service = CatalogoHotelService(MagicMock(), MagicMock())
    service.hoteis.get_by_id = MagicMock(return_value=hotel)
    service.catalogo.substituir_hotel = AsyncMock()

    asyncio.run(service.sincronizar_hotel(hotel_id))

    service.catalogo.substituir_hotel.assert_awaited_once()

    argumentos = service.catalogo.substituir_hotel.await_args.kwargs
    documento = argumentos["documento"]

    assert argumentos["hotel_id"] == str(hotel_id)
    assert documento["nome"] == "Hotel Teste"
    assert documento["categoria_estrelas"] == 4
    assert documento["cidade"]["nome"] == "Limoeiro do Norte"
    assert documento["comodidades"][0]["nome"] == "Piscina"
    assert documento["quartos"][0]["numero"] == "101"
    assert documento["quartos"][0]["preco_diaria"] == 250.0


def test_sincronizar_hotel_inexistente_lanca_erro():
    hotel_id = uuid4()

    service = CatalogoHotelService(MagicMock(), MagicMock())
    service.hoteis.get_by_id = MagicMock(return_value=None)
    service.catalogo.substituir_hotel = AsyncMock()

    try:
        asyncio.run(service.sincronizar_hotel(hotel_id))
        assert False, "Era esperado HotelNaoEncontradoParaCatalogoError"
    except HotelNaoEncontradoParaCatalogoError:
        pass

    service.catalogo.substituir_hotel.assert_not_called()


def test_substituir_hotel_usa_replace_one_com_upsert():
    mongo_db = MagicMock()
    repository = CatalogoHotelRepository(mongo_db)

    repository.collection.replace_one = AsyncMock()

    hotel_id = str(uuid4())
    documento = {
        "hotel_id": hotel_id,
        "nome": "Hotel Teste",
        "categoria_estrelas": 4,
    }

    asyncio.run(
        repository.substituir_hotel(
            hotel_id=hotel_id,
            documento=documento,
        )
    )

    repository.collection.replace_one.assert_awaited_once_with(
        {"hotel_id": hotel_id},
        documento,
        upsert=True,
    )

def test_buscar_por_filtros_filtra_por_cidade():
    mongo_db = MagicMock()
    repository = CatalogoHotelRepository(mongo_db)

    cursor = MagicMock()
    cursor.to_list = AsyncMock(return_value=[])
    repository.collection.find = MagicMock(return_value=cursor)

    asyncio.run(
        repository.buscar_por_filtros(cidade_id="cidade-123")
    )

    repository.collection.find.assert_called_once_with(
        {"cidade.id": "cidade-123"},
        {"_id": 0},
    )


def test_buscar_por_filtros_filtra_por_categoria_estrelas():
    mongo_db = MagicMock()
    repository = CatalogoHotelRepository(mongo_db)

    cursor = MagicMock()
    cursor.to_list = AsyncMock(return_value=[])
    repository.collection.find = MagicMock(return_value=cursor)

    asyncio.run(
        repository.buscar_por_filtros(categoria_estrelas=4)
    )

    repository.collection.find.assert_called_once_with(
        {"categoria_estrelas": 4},
        {"_id": 0},
    )


def test_buscar_por_filtros_filtra_por_cidade_e_categoria():
    mongo_db = MagicMock()
    repository = CatalogoHotelRepository(mongo_db)

    cursor = MagicMock()
    cursor.to_list = AsyncMock(return_value=[])
    repository.collection.find = MagicMock(return_value=cursor)

    asyncio.run(
        repository.buscar_por_filtros(
            cidade_id="cidade-123",
            categoria_estrelas=5,
        )
    )

    repository.collection.find.assert_called_once_with(
        {
            "cidade.id": "cidade-123",
            "categoria_estrelas": 5,
        },
        {"_id": 0},
    )