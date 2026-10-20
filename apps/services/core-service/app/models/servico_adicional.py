from decimal import Decimal
from uuid import UUID

from sqlalchemy import CheckConstraint, Numeric, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.uuid_utils import gerar_uuid7
from app.models.base import Base


class ServicoAdicional(Base):
    __tablename__ = "servicos_adicionais"

    __table_args__ = (
        CheckConstraint(
            "preco >= 0",
            name="ck_servicos_adicionais_preco_nao_negativo",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=gerar_uuid7,
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    preco: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )