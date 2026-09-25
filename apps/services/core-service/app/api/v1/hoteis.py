import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.core.database import get_db, get_mongo_db
from app.schemas.hotel import HotelCreateSchema, HotelResponseSchema
from app.services.catalogo_hotel_service import CatalogoHotelService
from app.services.hotel_service import (
    CidadeNaoEncontradaError,
    ComodidadeNaoEncontradaError,
    HotelNaoEncontradoError,
    HotelService,
)

router = APIRouter(prefix="/hoteis", tags=["Hoteis"])


@router.post(
    "",
    response_model=HotelResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um hotel vinculado a uma cidade",
)
async def criar_hotel(
    payload: HotelCreateSchema,
    db: Session = Depends(get_db),
    mongo_db=Depends(get_mongo_db),
    _admin=Depends(get_current_admin),
):
    service = HotelService(db)

    try:
        hotel = service.criar(
            nome=payload.nome,
            cidade_id=payload.cidade_id,
            categoria_estrelas=payload.categoria_estrelas,
        )

        await CatalogoHotelService(
            db,
            mongo_db,
        ).sincronizar_hotel(hotel.id)

        return hotel

    except CidadeNaoEncontradaError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.post(
    "/{hotel_id}/comodidades/{comodidade_id}",
    response_model=HotelResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Adiciona uma comodidade a um hotel",
)
async def adicionar_comodidade(
    hotel_id: uuid.UUID,
    comodidade_id: uuid.UUID,
    db: Session = Depends(get_db),
    mongo_db=Depends(get_mongo_db),
    _admin=Depends(get_current_admin),
):
    service = HotelService(db)

    try:
        hotel = service.adicionar_comodidade(
            hotel_id=hotel_id,
            comodidade_id=comodidade_id,
        )

        await CatalogoHotelService(
            db,
            mongo_db,
        ).sincronizar_hotel(hotel.id)

        return hotel

    except HotelNaoEncontradoError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e

    except ComodidadeNaoEncontradaError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.get(
    "/buscar",
    response_model=list[dict],
    summary="Busca hoteis no catalogo MongoDB",
)
async def buscar_hoteis(
    cidade_id: uuid.UUID | None = Query(
        default=None,
        description="Filtra os hoteis de uma cidade",
    ),
    categoria_estrelas: int | None = Query(
        default=None,
        ge=1,
        le=5,
        description="Filtra os hoteis pela categoria de estrelas",
    ),
    mongo_db=Depends(get_mongo_db),
):
    return await CatalogoHotelService(
        db=None,
        mongo_db=mongo_db,
    ).buscar_por_filtros(
        cidade_id=cidade_id,
        categoria_estrelas=categoria_estrelas,
    )


@router.get(
    "",
    response_model=list[HotelResponseSchema],
    summary="Lista os hoteis, com a cidade aninhada",
)
def listar_hoteis(
    cidade_id: uuid.UUID | None = Query(
        default=None,
        description="Filtra os hoteis de uma cidade especifica",
    ),
    db: Session = Depends(get_db),
):
    try:
        return HotelService(db).listar(cidade_id=cidade_id)

    except CidadeNaoEncontradaError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e