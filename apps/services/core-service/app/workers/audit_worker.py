import asyncio
import json
import logging
from datetime import datetime, timezone

import aio_pika
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def process_message(message: aio_pika.IncomingMessage):
    async with message.process(requeue=False):
        mongo_client = None

        try:
            data = json.loads(message.body.decode("utf-8"))

            if not isinstance(data, dict):
                raise ValueError("A mensagem deve ser um objeto JSON.")

            mongo_client = AsyncIOMotorClient(settings.MONGODB_URL)
            db = mongo_client[settings.MONGODB_DB]

            documento = {
                **data,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

            await db["logs_auditoria"].insert_one(documento)

            logger.info(
                "Auditoria salva no MongoDB: %s",
                data.get("evento", "sem_evento"),
            )

        except json.JSONDecodeError:
            logger.exception("Mensagem recebida não contém JSON válido.")

        except Exception:
            logger.exception("Erro ao processar mensagem de auditoria.")
            raise

        finally:
            if mongo_client is not None:
                mongo_client.close()


async def main():
    logger.info("Conectando ao RabbitMQ: %s", settings.RABBITMQ_URL)

    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)

        queue = await channel.declare_queue(
            "audit.logs",
            durable=True,
        )

        logger.info("Aguardando mensagens na fila audit.logs")

        await queue.consume(process_message)
        await asyncio.Future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Worker de auditoria encerrado.")
