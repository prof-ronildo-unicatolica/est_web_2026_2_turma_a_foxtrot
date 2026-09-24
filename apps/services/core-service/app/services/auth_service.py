from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.usuario import Usuario


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register(
        self,
        nome: str,
        email: str,
        senha: str,
    ) -> Usuario:
        usuario_existente = (
            self.db.query(Usuario)
            .filter(Usuario.email == email)
            .first()
        )

        if usuario_existente:
            raise ValueError("E-mail já cadastrado")

        usuario = Usuario(
            nome=nome,
            email=email,
            senha_hash=hash_password(senha),
            is_admin=False,
        )

        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)

        return usuario

    def login(
        self,
        email: str,
        senha: str,
    ) -> str | None:
        usuario = (
            self.db.query(Usuario)
            .filter(Usuario.email == email)
            .first()
        )

        if usuario is None:
            return None

        if not verify_password(senha, usuario.senha_hash):
            return None

        return create_access_token(str(usuario.id))