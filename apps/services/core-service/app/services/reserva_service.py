from datetime import date, timedelta
from decimal import Decimal

from app.models.tarifa_temporada import TarifaTemporada
from app.models.servico_adicional import ServicoAdicional


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


def calcular_adicional_criancas(
    total_diarias: Decimal,
    idades_criancas: list[int],
) -> Decimal:
    adicional = Decimal("0.00")

    for idade in idades_criancas:
        if 0 <= idade <= 5:
            continue

        if 6 <= idade <= 12:
            adicional += total_diarias * Decimal("0.50")

    return adicional

def calcular_adicional_horario(
    preco_diaria: Decimal,
    early_checkin: bool = False,
    late_checkout: bool = False,
) -> Decimal:
    adicional = Decimal("0.00")
    percentual = Decimal("0.30")

    if early_checkin:
        adicional += preco_diaria * percentual

    if late_checkout:
        adicional += preco_diaria * percentual

    return adicional

def calcular_servicos_adicionais(
    servicos: list[ServicoAdicional],
) -> Decimal:
    total = Decimal("0.00")

    for servico in servicos:
        total += servico.preco

    return total


def calcular_desconto_nao_reembolsavel(
    subtotal: Decimal,
    nao_reembolsavel: bool = False,
) -> Decimal:
    if not nao_reembolsavel:
        return Decimal("0.00")

    return subtotal * Decimal("0.10")

def calcular_total_reserva(
    preco_diaria: Decimal,
    data_checkin: date,
    data_checkout: date,
    tarifas_temporada: list[TarifaTemporada] | None = None,
    idades_criancas: list[int] | None = None,
    early_checkin: bool = False,
    late_checkout: bool = False,
    servicos: list[ServicoAdicional] | None = None,
    nao_reembolsavel: bool = False,
) -> Decimal:
    tarifas_temporada = tarifas_temporada or []
    idades_criancas = idades_criancas or []
    servicos = servicos or []

    total_diarias = calcular_diarias(
        preco_diaria=preco_diaria,
        data_checkin=data_checkin,
        data_checkout=data_checkout,
        tarifas_temporada=tarifas_temporada,
    )

    adicional_criancas = calcular_adicional_criancas(
        total_diarias=total_diarias,
        idades_criancas=idades_criancas,
    )

    adicional_horario = calcular_adicional_horario(
        preco_diaria=preco_diaria,
        early_checkin=early_checkin,
        late_checkout=late_checkout,
    )

    total_servicos = calcular_servicos_adicionais(
        servicos=servicos,
    )

    subtotal = (
        total_diarias
        + adicional_criancas
        + adicional_horario
        + total_servicos
    )

    desconto = calcular_desconto_nao_reembolsavel(
        subtotal=subtotal,
        nao_reembolsavel=nao_reembolsavel,
    )

    return subtotal - desconto