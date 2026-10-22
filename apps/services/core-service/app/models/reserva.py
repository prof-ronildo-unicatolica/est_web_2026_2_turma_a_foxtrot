
from datetime import date
from decimal import Decimal
from uuid import UUID

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.uuid_utils import gerar_uuid7
from app.models.base import Base


class Reserva(Base):
    __tablename__ = "reservas"

    __table_args__ = (
        CheckConstraint(
            "data_checkout > data_checkin",
            name="ck_reservas_periodo_valido",
        ),
        CheckConstraint(
            "quantidade_adultos >= 1",
            name="ck_reservas_adultos",
        ),
        CheckConstraint(
            "quantidade_criancas >= 0 AND quantidade_bebes >= 0",
            name="ck_reservas_criancas_bebes",
        ),
        CheckConstraint(
            "valor_total >= 0",
            name="ck_reservas_valor_total",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=gerar_uuid7,
    )

    usuario_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("usuarios.id"),
        nullable=False,
        index=True,
    )

    quarto_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("quartos.id"),
        nullable=False,
        index=True,
    )

    data_checkin: Mapped[date] = mapped_column(Date, nullable=False)
    data_checkout: Mapped[date] = mapped_column(Date, nullable=False)

    quantidade_adultos: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    quantidade_criancas: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    quantidade_bebes: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )

    early_checkin: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )
    late_checkout: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )
    necessita_berco: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )

    tarifa_tipo: Mapped[str] = mapped_column(
        String(30), nullable=False
    )

    data_limite_cancelamento: Mapped[date | None] = mapped_column(
        Date, nullable=True
    )
    valor_multa_cancelamento: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=0,
        server_default="0",
    )
    valor_total: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="Pendente",
        server_default="Pendente",
        index=True,
    )
