from datetime import date
from decimal import Decimal

from app.services.reserva_service import calcular_diarias


def test_calcular_diarias_basicas():
    total = calcular_diarias(
        preco_diaria=Decimal("200.00"),
        data_checkin=date(2026, 10, 1),
        data_checkout=date(2026, 10, 4),
    )

    assert total == Decimal("600.00")