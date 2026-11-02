
from datetime import timedelta
from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.core.rabbitmq import publish_event
from app.models.quarto import Quarto
from app.models.reserva import Reserva
from app.models.servico_adicional import ServicoAdicional
from app.models.tarifa_temporada import TarifaTemporada
from app.models.usuario import Usuario
from app.schemas.reserva import (
    ReservaCreate,
    ReservaCriadaResponse,
    ReservaResponse,
)
from app.services.reserva_service import calcular_total_reserva

router = APIRouter(prefix="/reservas", tags=["Reservas"])

FILA_RESERVAS = "solicitacoes-reserva"


@router.post(
    "",
    response_model=ReservaCriadaResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Solicita uma reserva assíncrona",
)
async def criar_reserva(
    payload: ReservaCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    # 1. Verifica se o quarto existe.
    quarto = (
        db.query(Quarto)
        .filter(Quarto.id == payload.quarto_id)
        .first()
    )

    if quarto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quarto não encontrado.",
        )

    # 2. Separa crianças de 0 a 5 anos das demais.
    idades_bebes = [
        idade for idade in payload.idades_criancas if idade <= 5
    ]
    idades_criancas = [
        idade for idade in payload.idades_criancas if idade >= 6
    ]

    if payload.quantidade_adultos > quarto.max_adultos:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Quantidade de adultos excede a capacidade do quarto.",
        )

    if len(idades_criancas) > quarto.max_criancas:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Quantidade de crianças excede a capacidade do quarto.",
        )

    # 3. Busca as tarifas sazonais aplicáveis.
    tarifas = (
        db.query(TarifaTemporada)
        .filter(
            TarifaTemporada.hotel_id == quarto.hotel_id,
            TarifaTemporada.data_inicio < payload.data_checkout,
            TarifaTemporada.data_fim >= payload.data_checkin,
        )
        .all()
    )

    # 4. Busca os serviços adicionais selecionados.
    servicos = []

    if payload.servicos_adicionais_ids:
        servicos = (
            db.query(ServicoAdicional)
            .filter(
                ServicoAdicional.id.in_(
                    payload.servicos_adicionais_ids
                )
            )
            .all()
        )

        if len(servicos) != len(payload.servicos_adicionais_ids):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Um ou mais serviços adicionais não existem.",
            )

    # 5. Calcula o valor no backend.
    try:
        valor_total = calcular_total_reserva(
            preco_diaria=Decimal(str(quarto.preco_diaria)),
            data_checkin=payload.data_checkin,
            data_checkout=payload.data_checkout,
            tarifas_temporada=tarifas,
            idades_criancas=payload.idades_criancas,
            early_checkin=payload.early_checkin,
            late_checkout=payload.late_checkout,
            servicos=servicos,
            nao_reembolsavel=(
                payload.tarifa_tipo == "nao_reembolsavel"
            ),
        )
    except (ValueError, ArithmeticError) as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Não foi possível calcular o preço da reserva.",
        ) from exc

    # 6. Cria a reserva pendente.
    reserva = Reserva(
        usuario_id=usuario.id,
        quarto_id=quarto.id,
        data_checkin=payload.data_checkin,
        data_checkout=payload.data_checkout,
        quantidade_adultos=payload.quantidade_adultos,
        quantidade_criancas=len(idades_criancas),
        quantidade_bebes=len(idades_bebes),
        early_checkin=payload.early_checkin,
        late_checkout=payload.late_checkout,
        necessita_berco=payload.necessita_berco,
        tarifa_tipo=payload.tarifa_tipo,
        data_limite_cancelamento=(
            payload.data_checkin - timedelta(days=1)
            if payload.tarifa_tipo == "flexivel"
            else None
        ),
        valor_multa_cancelamento=Decimal("0.00"),
        valor_total=valor_total,
        status="Pendente",
    )

    try:
        db.add(reserva)
        db.commit()
        db.refresh(reserva)
    except Exception:
        db.rollback()
        raise

    # 7. Envia a solicitação para o worker RabbitMQ.
    try:
        await publish_event(
            FILA_RESERVAS,
            {"reserva_id": str(reserva.id)},
        )
    except Exception as exc:
        # Tenta cancelar a reserva se ela ainda estiver pendente.
        try:
            db.refresh(reserva)
            if reserva.status == "Pendente":
                reserva.status = "Cancelada"
                db.commit()
        except Exception:
            db.rollback()

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "Não foi possível encaminhar a reserva para "
                "processamento. Consulte o estado da reserva "
                "antes de tentar novamente."
            ),
        ) from exc

    return ReservaCriadaResponse(
        id=reserva.id,
        status=reserva.status,
        mensagem="Reserva enviada para processamento.",
    )


@router.get(
    "/{reserva_id}",
    response_model=ReservaResponse,
    summary="Consulta o estado de uma reserva",
)
def consultar_reserva(
    reserva_id: UUID,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    reserva = (
        db.query(Reserva)
        .filter(
            Reserva.id == reserva_id,
            Reserva.usuario_id == usuario.id,
        )
        .first()
    )

    if reserva is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reserva não encontrada.",
        )

    return reserva
