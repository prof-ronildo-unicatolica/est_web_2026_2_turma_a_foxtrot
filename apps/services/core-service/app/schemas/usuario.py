from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    senha: str


class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UsuarioPublic(BaseModel):
    """Perfil publico do usuario (nunca expoe senha)."""

    email: EmailStr
    nome: str
    is_admin: bool
