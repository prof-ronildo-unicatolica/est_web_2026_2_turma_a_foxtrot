"""Testes da autenticacao JWT e RBAC."""

from app.core.security import hash_password
from app.models.usuario import Usuario


BASE = "/api/v1/auth"


def criar_usuario(db_session, nome, email, senha, is_admin=False):
    usuario = Usuario(
        nome=nome,
        email=email,
        senha_hash=hash_password(senha),
        is_admin=is_admin,
    )

    db_session.add(usuario)
    db_session.commit()
    db_session.refresh(usuario)

    return usuario


def fazer_login(client, email, senha):
    resp = client.post(
        f"{BASE}/login",
        json={"email": email, "senha": senha},
    )

    assert resp.status_code == 200

    return resp.json()["access_token"]


def test_register_cria_usuario(client):
    resp = client.post(
        f"{BASE}/register",
        json={
            "nome": "Cliente Teste",
            "email": "cliente@teste.com",
            "senha": "cliente123",
        },
    )

    assert resp.status_code == 201

    body = resp.json()

    assert body["nome"] == "Cliente Teste"
    assert body["email"] == "cliente@teste.com"
    assert body["is_admin"] is False
    assert "senha" not in body
    assert "senha_hash" not in body


def test_register_nao_permite_email_duplicado(client):
    payload = {
        "nome": "Cliente Teste",
        "email": "cliente@teste.com",
        "senha": "cliente123",
    }

    primeira = client.post(f"{BASE}/register", json=payload)
    segunda = client.post(f"{BASE}/register", json=payload)

    assert primeira.status_code == 201
    assert segunda.status_code == 409


def test_login_valido_retorna_token(client, db_session):
    criar_usuario(
        db_session,
        nome="Cliente Teste",
        email="cliente@teste.com",
        senha="cliente123",
    )

    resp = client.post(
        f"{BASE}/login",
        json={
            "email": "cliente@teste.com",
            "senha": "cliente123",
        },
    )

    assert resp.status_code == 200

    body = resp.json()

    assert body["token_type"] == "bearer"
    assert body["access_token"]


def test_login_invalido_retorna_401(client, db_session):
    criar_usuario(
        db_session,
        nome="Cliente Teste",
        email="cliente@teste.com",
        senha="cliente123",
    )

    resp = client.post(
        f"{BASE}/login",
        json={
            "email": "cliente@teste.com",
            "senha": "senha-errada",
        },
    )

    assert resp.status_code == 401


def test_rota_protegida_sem_token_e_bloqueada(client):
    resp = client.get(f"{BASE}/me")

    assert resp.status_code in (401, 403)


def test_rota_protegida_com_token_retorna_perfil(client, db_session):
    criar_usuario(
        db_session,
        nome="Cliente Teste",
        email="cliente@teste.com",
        senha="cliente123",
    )

    token = fazer_login(
        client,
        "cliente@teste.com",
        "cliente123",
    )

    resp = client.get(
        f"{BASE}/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert resp.status_code == 200

    body = resp.json()

    assert body["email"] == "cliente@teste.com"
    assert body["nome"] == "Cliente Teste"
    assert body["is_admin"] is False
    assert "senha" not in body
    assert "senha_hash" not in body


def test_token_invalido_bloqueia_rota_protegida(client):
    resp = client.get(
        f"{BASE}/me",
        headers={"Authorization": "Bearer token-invalido"},
    )

    assert resp.status_code == 401


def test_cliente_nao_acessa_rota_admin(client, db_session):
    criar_usuario(
        db_session,
        nome="Cliente Teste",
        email="cliente@teste.com",
        senha="cliente123",
        is_admin=False,
    )

    token = fazer_login(
        client,
        "cliente@teste.com",
        "cliente123",
    )

    resp = client.get(
        f"{BASE}/admin/verificacao",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert resp.status_code == 403


def test_admin_acessa_rota_admin(client, db_session):
    criar_usuario(
        db_session,
        nome="Administrador Teste",
        email="admin@teste.com",
        senha="admin123",
        is_admin=True,
    )

    token = fazer_login(
        client,
        "admin@teste.com",
        "admin123",
    )

    resp = client.get(
        f"{BASE}/admin/verificacao",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert resp.status_code == 200

    body = resp.json()

    assert body["email"] == "admin@teste.com"