from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.core.database import get_db
from app.schemas.hotel import CidadeCreateSchema, CidadeResponseSchema
from app.services.hotel_service import CidadeJaExisteError, CidadeService

router = APIRouter(prefix="/cidades", tags=["Cidades"])


@router.post(
    "",
    response_model=CidadeResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Cria uma cidade",
)
def criar_cidade(
    payload: CidadeCreateSchema,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    service = CidadeService(db)

    try:
        return service.criar(
            nome=payload.nome,
            limite_territorial=payload.limite_territorial,  
        )
    except CidadeJaExisteError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )


@router.get(
    "",
    response_model=list[CidadeResponseSchema],
    summary="Lista as cidades",
)
def listar_cidades(db: Session = Depends(get_db)):
    return CidadeService(db).listar()