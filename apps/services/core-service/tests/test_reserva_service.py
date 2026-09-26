from datetime import date
from decimal import Decimal
from uuid import uuid4

from app.models.tarifa_temporada import TarifaTemporada
from app.services.reserva_service import calcular_diarias


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