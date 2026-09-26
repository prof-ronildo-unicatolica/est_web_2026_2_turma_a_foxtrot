from datetime import date
from decimal import Decimal
from uuid import uuid4

from app.models.tarifa_temporada import TarifaTemporada
from app.services.reserva_service import (
    calcular_adicional_criancas,
    calcular_adicional_horario,
    calcular_diarias,
)

def test_calcular_diarias_basicas():
    total = calcular_diarias(
        preco_diaria=Decimal("200.00"),
        data_checkin=date(2026, 10, 1),
        data_checkout=date(2026, 10, 4),
    )

    assert total == Decimal("600.00")


def test_calcular_diarias_com_tarifa_temporada():
    tarifa = TarifaTemporada(
        hotel_id=uuid4(),
        nome="Alta temporada",
        data_inicio=date(2026, 12, 21),
        data_fim=date(2026, 12, 22),
        multiplicador=Decimal("1.50"),
    )

    total = calcular_diarias(
        preco_diaria=Decimal("200.00"),
        data_checkin=date(2026, 12, 20),
        data_checkout=date(2026, 12, 23),
        tarifas_temporada=[tarifa],
    )

    assert total == Decimal("800.00")


def test_bebe_de_0_a_5_anos_nao_paga_adicional():
    adicional = calcular_adicional_criancas(
        total_diarias=Decimal("600.00"),
        idades_criancas=[4],
    )

    assert adicional == Decimal("0.00")


def test_crianca_de_6_a_12_anos_paga_50_porcento():
    adicional = calcular_adicional_criancas(
        total_diarias=Decimal("600.00"),
        idades_criancas=[8],
    )

    assert adicional == Decimal("300.00")

def test_early_checkin_acrescenta_30_porcento_da_diaria():
    adicional = calcular_adicional_horario(
        preco_diaria=Decimal("200.00"),
        early_checkin=True,
        late_checkout=False,
    )

    assert adicional == Decimal("60.00")


def test_late_checkout_acrescenta_30_porcento_da_diaria():
    adicional = calcular_adicional_horario(
        preco_diaria=Decimal("200.00"),
        early_checkin=False,
        late_checkout=True,
    )

    assert adicional == Decimal("60.00")


def test_early_checkin_e_late_checkout_somam_os_adicionais():
    adicional = calcular_adicional_horario(
        preco_diaria=Decimal("200.00"),
        early_checkin=True,
        late_checkout=True,
    )

    assert adicional == Decimal("120.00")