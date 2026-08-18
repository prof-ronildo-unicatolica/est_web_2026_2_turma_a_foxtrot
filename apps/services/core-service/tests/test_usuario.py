from uuid import UUID

from app.models.usuario import Usuario


def test_criar_usuario_com_uuidv7(db_session):
    usuario = Usuario(
        nome="Usuario Teste",
        email="usuario@teste.com",
        senha_hash="hash_de_teste",
    )

    db_session.add(usuario)
    db_session.commit()
    db_session.refresh(usuario)

    assert isinstance(usuario.id, UUID)
    assert usuario.id.version == 7
    assert usuario.nome == "Usuario Teste"
    assert usuario.email == "usuario@teste.com"
    assert usuario.senha_hash == "hash_de_teste"
    assert usuario.is_admin is False