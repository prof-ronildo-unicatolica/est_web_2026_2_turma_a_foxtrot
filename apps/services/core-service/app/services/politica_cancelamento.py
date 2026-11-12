
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP
from typing import Literal


TipoTarifa = Literal["flexivel", "nao_reembolsavel"]

CENTAVOS = Decimal("0.01")
ZERO = Decimal("0.00")


def calcular_data_limite_cancelamento(
    data_checkin: date,
    tarifa_tipo: TipoTarifa,
) -> date | None:
    """
    Retorna o prazo limite de cancelamento gratuito.

    Tarifas flexíveis: dois dias antes do check-in.
    Tarifas não reembolsáveis: não possuem cancelamento gratuito.
    """
    if tarifa_tipo == "nao_reembolsavel":
        return None

    if tarifa_tipo != "flexivel":
        raise ValueError("Tipo de tarifa inválido.")

    return data_checkin - timedelta(days=2)


def calcular_multa_cancelamento(
    tarifa_tipo: TipoTarifa,
    data_checkin: date,
    data_cancelamento: date,
    valor_total: Decimal,
    valor_diaria: Decimal,
) -> Decimal:
    """
    Calcula a multa de cancelamento.

    Flexível:
      - Até dois dias antes do check-in: sem multa.
      - Depois do prazo: multa de uma diária.

    Não reembolsável:
      - Multa de 100% do valor total da reserva.
    """
    if tarifa_tipo not in ("flexivel", "nao_reembolsavel"):
        raise ValueError("Tipo de tarifa inválido.")

    if valor_total < ZERO or valor_diaria < ZERO:
        raise ValueError("Os valores não podem ser negativos.")

    if tarifa_tipo == "nao_reembolsavel":
        multa = valor_total
    else:
        data_limite = calcular_data_limite_cancelamento(
            data_checkin=data_checkin,
            tarifa_tipo=tarifa_tipo,
        )

        if data_cancelamento <= data_limite:
            multa = ZERO
        else:
            multa = valor_diaria

    return multa.quantize(CENTAVOS, rounding=ROUND_HALF_UP)
