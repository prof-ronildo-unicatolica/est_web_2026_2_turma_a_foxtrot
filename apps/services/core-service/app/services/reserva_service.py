from datetime import date, timedelta
from decimal import Decimal

from app.models.tarifa_temporada import TarifaTemporada


def calcular_diarias(
    preco_diaria: Decimal,
    data_checkin: date,
    data_checkout: date,
    tarifas_temporada: list[TarifaTemporada] | None = None,
) -> Decimal:
    tarifas_temporada = tarifas_temporada or []

    total = Decimal("0.00")
    data_diaria = data_checkin

    while data_diaria < data_checkout:
        valor_diaria = preco_diaria

        for tarifa in tarifas_temporada:
            if tarifa.data_inicio <= data_diaria <= tarifa.data_fim:
                valor_diaria *= tarifa.multiplicador
                break

        total += valor_diaria
        data_diaria += timedelta(days=1)

    return total