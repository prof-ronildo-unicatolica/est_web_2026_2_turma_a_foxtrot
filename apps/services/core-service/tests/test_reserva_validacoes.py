from datetime import date, timedelta
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.schemas.reserva import ReservaCreate


def payload_reserva_valida():
    hoje = date.today()

    return {
        "quarto_id": str(uuid4()),
        "data_checkin": hoje + timedelta(days=1),
        "data_checkout": hoje + timedelta(days=2),
        "quantidade_adultos": 1,
    }


def test_reserva_com_dados_validos():
    reserva = ReservaCreate(**payload_reserva_valida())

    assert reserva.quantidade_adultos == 1
    assert reserva.idades_criancas == []
    assert reserva.tarifa_tipo == "flexivel"


def test_checkin_no_passado_e_invalido():
    payload = payload_reserva_valida()
    payload["data_checkin"] = date.today() - timedelta(days=1)

    with pytest.raises(ValidationError):
        ReservaCreate(**payload)


def test_checkout_igual_ao_checkin_e_invalido():
    payload = payload_reserva_valida()
    payload["data_checkout"] = payload["data_checkin"]

    with pytest.raises(ValidationError):
        ReservaCreate(**payload)


def test_checkout_anterior_ao_checkin_e_invalido():
    payload = payload_reserva_valida()
    payload["data_checkout"] = (
        payload["data_checkin"] - timedelta(days=1)
    )

    with pytest.raises(ValidationError):
        ReservaCreate(**payload)


@pytest.mark.parametrize("idade", [-1, 13])
def test_idade_de_crianca_fora_do_intervalo_e_invalida(idade):
    payload = payload_reserva_valida()
    payload["idades_criancas"] = [idade]

    with pytest.raises(ValidationError):
        ReservaCreate(**payload)


def test_idades_limite_de_criancas_sao_validas():
    payload = payload_reserva_valida()
    payload["idades_criancas"] = [0, 5, 6, 12]

    reserva = ReservaCreate(**payload)

    assert reserva.idades_criancas == [0, 5, 6, 12]


def test_servicos_adicionais_duplicados_sao_invalidos():
    servico_id = str(uuid4())

    payload = payload_reserva_valida()
    payload["servicos_adicionais_ids"] = [
        servico_id,
        servico_id,
    ]

    with pytest.raises(ValidationError):
        ReservaCreate(**payload)


def test_servicos_adicionais_sem_duplicidade_sao_validos():
    payload = payload_reserva_valida()
    payload["servicos_adicionais_ids"] = [
        str(uuid4()),
        str(uuid4()),
    ]

    reserva = ReservaCreate(**payload)

    assert len(reserva.servicos_adicionais_ids) == 2