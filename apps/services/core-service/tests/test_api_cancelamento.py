"""Testes de integração da API de cancelamento de reservas.

Executar a partir de apps/services/core-service:
    python -m pytest tests/test_api_cancelamento.py -v
"""

from datetime import date, timedelta
from decimal import Decimal
from unittest.mock import AsyncMock, patch

import pytest

from app.core.security import hash_password
from app.models.cidade import Cidade
from app.models.hotel import Hotel
from app.models.quarto import Quarto
from app.models.reserva import Reserva
from app.models.usuario import Usuario

BASE = "/api/v1/reservas"
SENHA = "senha123"


def criar_usuario(db_session, email):
    usuario = Usuario(
        nome="Cliente de Teste",
        email=email,
        senha_hash=hash_password(SENHA),
        is_admin=False,
    )
    db_session.add(usuario)
    db_session.flush()
    return usuario


def autenticar(client, email):
    resposta = client.post(
        "/api/v1/auth/login",
        json={"email": email, "senha": SENHA},
    )
    assert resposta.status_code == 200, resposta.text
    token = resposta.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def criar_cenario(
    db_session,
    *,
    tarifa_tipo="flexivel",
    dias_ate_checkin=5,
    status="Confirmada",
    email="titular@teste.com",
):
    """Cria dados reais no SQLite de testes, sem depender de MongoDB/RabbitMQ."""
    usuario = criar_usuario(db_session, email)

    cidade = Cidade(nome="Cidade Teste Cancelamento")
    db_session.add(cidade)
    db_session.flush()

    hotel = Hotel(nome="Hotel Teste", categoria_estrelas=3, cidade_id=cidade.id)
    db_session.add(hotel)
    db_session.flush()

    quarto = Quarto(
        hotel_id=hotel.id,
        numero="101",
        tipo="Standard",
        preco_diaria=Decimal("150.00"),
        max_adultos=2,
        max_criancas=0,
    )
    db_session.add(quarto)
    db_session.flush()

    checkin = date.today() + timedelta(days=dias_ate_checkin)
    reserva = Reserva(
        usuario_id=usuario.id,
        quarto_id=quarto.id,
        data_checkin=checkin,
        data_checkout=checkin + timedelta(days=2),
        quantidade_adultos=1,
        quantidade_criancas=0,
        quantidade_bebes=0,
        tarifa_tipo=tarifa_tipo,
        valor_total=Decimal("300.00"),
        status=status,
    )
    db_session.add(reserva)
    db_session.commit()
    return reserva


def solicitar_cancelamento(client, reserva_id, headers):
    return client.post(f"{BASE}/{reserva_id}/cancelar", headers=headers)


@pytest.mark.parametrize(
    "tarifa_tipo,dias_ate_checkin,multa_esperada",
    [
        ("flexivel", 5, Decimal("0.00")),
        ("flexivel", 1, Decimal("150.00")),
        ("nao_reembolsavel", 5, Decimal("300.00")),
        ("flexivel", 2, Decimal("0.00")),  # No dia limite: sem multa.
    ],
    ids=[
        "flexivel_sem_multa",
        "flexivel_fora_do_prazo",
        "nao_reembolsavel_multa_total",
        "flexivel_no_dia_limite",
    ],
)
def test_cancelamento_calcula_multa_e_publica_evento(
    client, db_session, tarifa_tipo, dias_ate_checkin, multa_esperada
):
    reserva = criar_cenario(
        db_session,
        tarifa_tipo=tarifa_tipo,
        dias_ate_checkin=dias_ate_checkin,
    )
    headers = autenticar(client, "titular@teste.com")

    with patch("app.api.v1.reservas.publish_event", new_callable=AsyncMock) as publicar:
        resposta = solicitar_cancelamento(client, reserva.id, headers)

    assert resposta.status_code == 200, resposta.text
    dados = resposta.json()
    assert dados["reserva_id"] == str(reserva.id)
    assert dados["status"] == "Cancelada"
    assert Decimal(dados["valor_multa_cancelamento"]) == multa_esperada

    db_session.refresh(reserva)
    assert reserva.status == "Cancelada"
    assert reserva.valor_multa_cancelamento == multa_esperada

    publicar.assert_awaited_once()
    fila, evento = publicar.await_args.args
    assert fila == "audit.logs"
    assert evento["evento"] == "reserva.cancelada"
    assert evento["reserva_id"] == str(reserva.id)
    assert evento["usuario_id"] == str(reserva.usuario_id)
    assert evento["status"] == "Cancelada"
    assert Decimal(evento["valor_multa_cancelamento"]) == multa_esperada


def test_cancelamento_sem_autenticacao(client):
    resposta = client.post(f"{BASE}/00000000-0000-0000-0000-000000000001/cancelar")
    assert resposta.status_code in (401, 403)


def test_outro_usuario_nao_pode_cancelar_reserva_ativa(client, db_session):
    reserva = criar_cenario(db_session)
    criar_usuario(db_session, "outro@teste.com")
    db_session.commit()
    headers_outro = autenticar(client, "outro@teste.com")

    with patch("app.api.v1.reservas.publish_event", new_callable=AsyncMock) as publicar:
        resposta = solicitar_cancelamento(client, reserva.id, headers_outro)

    assert resposta.status_code == 404, resposta.text
    db_session.refresh(reserva)
    assert reserva.status == "Confirmada"
    publicar.assert_not_awaited()


def test_cancelamento_duplicado_retorna_409(client, db_session):
    reserva = criar_cenario(db_session)
    headers = autenticar(client, "titular@teste.com")

    with patch("app.api.v1.reservas.publish_event", new_callable=AsyncMock) as publicar:
        primeira = solicitar_cancelamento(client, reserva.id, headers)
        segunda = solicitar_cancelamento(client, reserva.id, headers)

    assert primeira.status_code == 200, primeira.text
    assert segunda.status_code == 409, segunda.text
    db_session.refresh(reserva)
    assert reserva.status == "Cancelada"
    publicar.assert_awaited_once()


def test_reserva_inexistente_retorna_404(client, db_session):
    criar_usuario(db_session, "titular@teste.com")
    db_session.commit()
    headers = autenticar(client, "titular@teste.com")

    with patch("app.api.v1.reservas.publish_event", new_callable=AsyncMock) as publicar:
        resposta = solicitar_cancelamento(
            client, "00000000-0000-0000-0000-000000000001", headers
        )

    assert resposta.status_code == 404, resposta.text
    publicar.assert_not_awaited()


def test_status_nao_cancelavel_retorna_409(client, db_session):
    reserva = criar_cenario(db_session, status="Concluida")
    headers = autenticar(client, "titular@teste.com")

    with patch("app.api.v1.reservas.publish_event", new_callable=AsyncMock) as publicar:
        resposta = solicitar_cancelamento(client, reserva.id, headers)

    assert resposta.status_code == 409, resposta.text
    db_session.refresh(reserva)
    assert reserva.status == "Concluida"
    publicar.assert_not_awaited()


def test_tarifa_invalida_retorna_422_sem_cancelar(client, db_session):
    reserva = criar_cenario(db_session, tarifa_tipo="tarifa_invalida")
    headers = autenticar(client, "titular@teste.com")

    with patch("app.api.v1.reservas.publish_event", new_callable=AsyncMock) as publicar:
        resposta = solicitar_cancelamento(client, reserva.id, headers)

    assert resposta.status_code == 422, resposta.text
    db_session.refresh(reserva)
    assert reserva.status == "Confirmada"
    publicar.assert_not_awaited()


def test_falha_auditoria_retorna_503_mas_reserva_ja_cancelada(client, db_session):
    """Documenta o comportamento atual: commit ocorre antes da publicação."""
    reserva = criar_cenario(db_session)
    headers = autenticar(client, "titular@teste.com")

    with patch("app.api.v1.reservas.publish_event", new_callable=AsyncMock) as publicar:
        publicar.side_effect = RuntimeError("RabbitMQ indisponivel")
        resposta = solicitar_cancelamento(client, reserva.id, headers)

    assert resposta.status_code == 503, resposta.text
    db_session.refresh(reserva)
    assert reserva.status == "Cancelada"
    publicar.assert_awaited_once()