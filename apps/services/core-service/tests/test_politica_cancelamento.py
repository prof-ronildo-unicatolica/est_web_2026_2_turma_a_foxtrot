
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
