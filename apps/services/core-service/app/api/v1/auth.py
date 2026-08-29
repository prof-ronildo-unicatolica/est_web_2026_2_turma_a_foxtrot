from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import autenticar_credenciais, get_current_admin, get_current_user
from app.core.database import get_db
from app.core.security import criar_access_token
from app.models.usuario import Usuario
from app.schemas.usuario import LoginRequest, Token, UsuarioPublic

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=Token)
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db),
):
    usuario = autenticar_credenciais(
        payload.email,
        payload.senha,
        db,
    )

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = criar_access_token(usuario.email)

    return Token(
        access_token=access_token,
        token_type="bearer",
    )


@router.get("/me", response_model=UsuarioPublic)
def get_me(
    usuario_atual: Usuario = Depends(get_current_user),
):
    return usuario_atual


@router.get("/admin/verificacao")
def somente_admin(
    admin: Usuario = Depends(get_current_admin),
):
    return {
        "mensagem": f"Acesso administrativo concedido para {admin.nome}"
    }
