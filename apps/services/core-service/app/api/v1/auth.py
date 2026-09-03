from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.schemas.usuario import (
    LoginRequest,
    RegisterRequest,
    Token,
    UsuarioPublic,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=UsuarioPublic,
    status_code=status.HTTP_201_CREATED,
)
def register(
    payload: RegisterRequest,
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    try:
        usuario = service.register(
            nome=payload.nome,
            email=payload.email,
            senha=payload.senha,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    return usuario


@router.post("/login", response_model=Token)
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    token = service.login(
        email=payload.email,
        senha=payload.senha,
    )

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return Token(access_token=token)


@router.get("/me", response_model=UsuarioPublic)
def get_me(
    usuario_atual=Depends(get_current_user),
):
    return usuario_atual