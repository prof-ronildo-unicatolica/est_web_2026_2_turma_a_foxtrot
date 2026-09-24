from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.core.database import get_db
from app.schemas.hotel import (
    ComodidadeCreateSchema,
    ComodidadeResponseSchema,
)
from app.services.comodidade_service import (
    ComodidadeJaExisteError,
    ComodidadeService,
)

router = APIRouter(
    prefix="/comodidades",
    tags=["Comodidades"],
)


@router.post(
    "",
    response_model=ComodidadeResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Cria uma comodidade",
)
def criar_comodidade(
    payload: ComodidadeCreateSchema,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    service = ComodidadeService(db)

    try:
        return service.criar(nome=payload.nome)
    except ComodidadeJaExisteError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        ) from e


@router.get(
    "",
    response_model=list[ComodidadeResponseSchema],
    summary="Lista as comodidades",
)
def listar_comodidades(
    db: Session = Depends(get_db),
):
    return ComodidadeService(db).listar()