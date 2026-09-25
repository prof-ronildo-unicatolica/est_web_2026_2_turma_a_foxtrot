from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.core.database import get_db, get_mongo_db
from app.schemas.hotel import (
    QuartoCreateSchema,
    QuartoResponseSchema,
)
from app.services.catalogo_hotel_service import CatalogoHotelService
from app.services.quarto_service import (
    HotelNaoEncontradoError,
    QuartoNaoEncontradoError,
    QuartoService,
)

router = APIRouter(
    prefix="/quartos",
    tags=["Quartos"],
)


@router.post(
    "",
    response_model=QuartoResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um quarto",
)
async def criar_quarto(
    payload: QuartoCreateSchema,
    db: Session = Depends(get_db),
    mongo_db=Depends(get_mongo_db),
    _admin=Depends(get_current_admin),
):
    service = QuartoService(db)

    try:
        quarto = service.criar(
            hotel_id=payload.hotel_id,
            numero=payload.numero,
            tipo=payload.tipo,
            preco_diaria=payload.preco_diaria,
            max_adultos=payload.max_adultos,
            max_criancas=payload.max_criancas,
        )

        await CatalogoHotelService(
            db,
            mongo_db,
        ).sincronizar_hotel(quarto.hotel_id)

        return quarto
    
    except HotelNaoEncontradoError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e

@router.get(
    "/hotel/{hotel_id}",
    response_model=list[QuartoResponseSchema],
    summary="Lista os quartos de um hotel",
)
def listar_quartos_por_hotel(
    hotel_id: UUID,
    db: Session = Depends(get_db),
):
    service = QuartoService(db)

    try:
        return service.listar_por_hotel(hotel_id)
    except HotelNaoEncontradoError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.put(
    "/{quarto_id}",
    response_model=QuartoResponseSchema,
    summary="Atualiza um quarto",
)
async def atualizar_quarto(
    quarto_id: UUID,
    payload: QuartoCreateSchema,
    db: Session = Depends(get_db),
    mongo_db=Depends(get_mongo_db),
    _admin=Depends(get_current_admin),
):
    service = QuartoService(db)

    try:
        quarto = service.atualizar(
            quarto_id=quarto_id,
            numero=payload.numero,
            tipo=payload.tipo,
            preco_diaria=payload.preco_diaria,
            max_adultos=payload.max_adultos,
            max_criancas=payload.max_criancas,
        )

        await CatalogoHotelService(
            db,
            mongo_db,
        ).sincronizar_hotel(quarto.hotel_id)

        return quarto

    except QuartoNaoEncontradoError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.delete(
    "/{quarto_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Exclui um quarto",
)
async def excluir_quarto(
    quarto_id: UUID,
    db: Session = Depends(get_db),
    mongo_db=Depends(get_mongo_db),
    _admin=Depends(get_current_admin),
):
    service = QuartoService(db)

    try:
        quarto = service.buscar(quarto_id)
        hotel_id = quarto.hotel_id

        service.excluir(quarto_id)

        await CatalogoHotelService(
            db,
            mongo_db,
        ).sincronizar_hotel(hotel_id)

    except QuartoNaoEncontradoError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e

    