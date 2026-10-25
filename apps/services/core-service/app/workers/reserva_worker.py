
import asyncio
import json
import logging
from decimal import Decimal
from uuid import UUID

import aio_pika
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import SessionLocal, get_mongo_db
from app.core.rabbitmq import publish_event

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FILA_RESERVAS = "solicitacoes-reserva"
FILA_AUDITORIA = "audit.logs"


def processar_reserva(db: Session, reserva_id: UUID) -> dict:
    """Processa uma reserva existente no PostgreSQL."""

    reserva = db.execute(
        text("""
            SELECT
                id,
                usuario_id,
                quarto_id,
                data_checkin AS checkin,
                data_checkout AS checkout,
                quantidade_adultos AS adultos,
                quantidade_criancas AS criancas,
                valor_total,
                status
            FROM reservas
            WHERE id = :id
            FOR UPDATE
        """),
        {"id": reserva_id},
    ).mappings().first()

    if not reserva:
        raise ValueError(f"Reserva {reserva_id} nao encontrada.")

    resultado_base = {
        "evento": "reserva.processada",
        "reserva_id": str(reserva_id),
        "usuario_id": str(reserva["usuario_id"]),
        "quarto_id": str(reserva["quarto_id"]),
        "valor_total": str(Decimal(str(reserva["valor_total"]))),
    }

    if reserva["status"] != "Pendente":
        db.commit()
        return {
            **resultado_base,
            "status": reserva["status"],
            "motivo": "Reserva ja processada anteriormente.",
        }

    checkin = reserva["checkin"]
    checkout = reserva["checkout"]

    if checkout <= checkin:
        raise ValueError("O checkout deve ser posterior ao check-in.")
    
    
    # Bloqueia o quarto para serializar o processamento das reservas.
    db.execute(
        text("""
            SELECT id
            FROM quartos
            WHERE id = :quarto_id
            FOR UPDATE
        """),
        {"quarto_id": reserva["quarto_id"]},
    ).first()


    conflito = db.execute(
        text("""
            SELECT id
            FROM reservas
            WHERE quarto_id = :quarto_id
              AND id <> :reserva_id
              AND status = 'Confirmada'
              AND data_checkin < :checkout
              AND data_checkout > :checkin
            LIMIT 1
        """),
        {
            "quarto_id": reserva["quarto_id"],
            "reserva_id": reserva_id,
            "checkin": checkin,
            "checkout": checkout,
        },
    ).first()

    status_final = "Cancelada" if conflito else "Confirmada"

    motivo = (
        "Conflito de datas com outra reserva confirmada."
        if conflito
        else None
    )

    db.execute(
        text("""
            UPDATE reservas
            SET status = :status
            WHERE id = :id AND status = 'Pendente'
        """),
        {"id": reserva_id, "status": status_final},
    )
    db.commit()

    return {
        **resultado_base,
        "status": status_final,
        "motivo": motivo,
    }


async def processar_mensagem(message: aio_pika.IncomingMessage):
    async with message.process(requeue=False):
        db: Session = SessionLocal()

        try:
            data = json.loads(message.body.decode("utf-8"))

            if not isinstance(data, dict):
                raise ValueError("A mensagem deve ser um objeto JSON.")

            if "reserva_id" not in data:
                raise ValueError("Campo reserva_id ausente na mensagem.")

            reserva_id = UUID(str(data["reserva_id"]))

            # Simulacao do processamento do pagamento.
            await asyncio.sleep(2)

            resultado = processar_reserva(db, reserva_id)

            # Registra o resultado no historico de auditoria.
            mongo_db = get_mongo_db()
            await mongo_db["historico_auditoria"].insert_one(
                resultado.copy()
            )

            # Publica o evento para o worker de auditoria.
            await publish_event(FILA_AUDITORIA, resultado)

            logger.info(
                "Reserva %s finalizada com status %s",
                resultado["reserva_id"],
                resultado["status"],
            )

        except (ValueError, KeyError, TypeError) as exc:
            db.rollback()
            logger.warning(
                "Mensagem invalida ou reserva invalida: %s", exc
            )

        except Exception:
            db.rollback()
            logger.exception("Falha ao processar solicitacao de reserva.")
            raise

        finally:
            db.close()


async def main():
    logger.info("Conectando ao RabbitMQ: %s", settings.RABBITMQ_URL)

    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)

        queue = await channel.declare_queue(
            FILA_RESERVAS,
            durable=True,
        )

        logger.info("Aguardando mensagens em %s", FILA_RESERVAS)

        await queue.consume(processar_mensagem)
        await asyncio.Future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Worker encerrado.")
