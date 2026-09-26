from datetime import date
from decimal import Decimal


def calcular_diarias(
    preco_diaria: Decimal,
    data_checkin: date,
    data_checkout: date,
) -> Decimal:
    quantidade_diarias = (data_checkout - data_checkin).days

    return preco_diaria * quantidade_diarias