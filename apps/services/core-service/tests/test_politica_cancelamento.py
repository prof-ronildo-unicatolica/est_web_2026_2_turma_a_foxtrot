
from datetime import date
from decimal import Decimal

import pytest

from app.services.politica_cancelamento import (
    calcular_data_limite_cancelamento,
    calcular_multa_cancelamento,
)


def test_tarifa_flexivel_cancelada_com_antecedencia():
    multa = calcular_multa_cancelamento(
        tarifa_tipo="flexivel",
        data_checkin=date(2026, 12, 20),
        data_cancelamento=date(2026, 12, 18),
        valor_total=Decimal("1000.00"),
        valor_diaria=Decimal("200.00"),
    )

    assert multa == Decimal("0.00")


def test_tarifa_flexivel_cancelada_fora_do_prazo():
    multa = calcular_multa_cancelamento(
        tarifa_tipo="flexivel",
        data_checkin=date(2026, 12, 20),
        data_cancelamento=date(2026, 12, 19),
        valor_total=Decimal("1000.00"),
        valor_diaria=Decimal("200.00"),
    )

    assert multa == Decimal("200.00")


def test_tarifa_nao_reembolsavel_com_antecedencia():
    multa = calcular_multa_cancelamento(
        tarifa_tipo="nao_reembolsavel",
        data_checkin=date(2026, 12, 20),
        data_cancelamento=date(2026, 12, 15),
        valor_total=Decimal("1000.00"),
        valor_diaria=Decimal("200.00"),
    )

    assert multa == Decimal("1000.00")


def test_tarifa_nao_reembolsavel_fora_do_prazo():
    multa = calcular_multa_cancelamento(
        tarifa_tipo="nao_reembolsavel",
        data_checkin=date(2026, 12, 20),
        data_cancelamento=date(2026, 12, 19),
        valor_total=Decimal("1000.00"),
        valor_diaria=Decimal("200.00"),
    )

    assert multa == Decimal("1000.00")


def test_data_limite_flexivel():
    limite = calcular_data_limite_cancelamento(
        data_checkin=date(2026, 12, 20),
        tarifa_tipo="flexivel",
    )

    assert limite == date(2026, 12, 18)


def test_data_limite_nao_reembolsavel():
    limite = calcular_data_limite_cancelamento(
        data_checkin=date(2026, 12, 20),
        tarifa_tipo="nao_reembolsavel",
    )

    assert limite is None


def test_valores_negativos_sao_invalidos():
    with pytest.raises(ValueError):
        calcular_multa_cancelamento(
            tarifa_tipo="flexivel",
            data_checkin=date(2026, 12, 20),
            data_cancelamento=date(2026, 12, 19),
            valor_total=Decimal("-100.00"),
            valor_diaria=Decimal("200.00"),
        )

def test_tipo_tarifa_invalido_nao_calcula_multa():
    with pytest.raises(ValueError, match="Tipo de tarifa inválido"):
        calcular_multa_cancelamento(
            tarifa_tipo="tarifa_inexistente",
            data_checkin=date(2026, 12, 20),
            data_cancelamento=date(2026, 12, 18),
            valor_total=Decimal("1000.00"),
            valor_diaria=Decimal("200.00"),
        )


def test_valor_diaria_negativo_e_invalido():
    with pytest.raises(ValueError, match="Os valores não podem ser negativos"):
        calcular_multa_cancelamento(
            tarifa_tipo="flexivel",
            data_checkin=date(2026, 12, 20),
            data_cancelamento=date(2026, 12, 19),
            valor_total=Decimal("1000.00"),
            valor_diaria=Decimal("-200.00"),
        )


def test_multa_e_arredondada_para_duas_casas_decimais():
    multa = calcular_multa_cancelamento(
        tarifa_tipo="flexivel",
        data_checkin=date(2026, 12, 20),
        data_cancelamento=date(2026, 12, 19),
        valor_total=Decimal("1000.00"),
        valor_diaria=Decimal("200.567"),
    )

    assert multa == Decimal("200.57")


def test_data_limite_com_tipo_tarifa_invalido():
    with pytest.raises(ValueError, match="Tipo de tarifa inválido"):
        calcular_data_limite_cancelamento(
            data_checkin=date(2026, 12, 20),
            tarifa_tipo="tarifa_inexistente",
        )