from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import CheckConstraint, Date, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.uuid_utils import gerar_uuid7
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.hotel import Hotel


class TarifaTemporada(Base):
    __tablename__ = "tarifas_temporada"

    __table_args__ = (
        CheckConstraint(
            "data_fim >= data_inicio",
            name="ck_tarifas_temporada_periodo_valido",
        ),
        CheckConstraint(
            "multiplicador > 0",
            name="ck_tarifas_temporada_multiplicador_positivo",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=gerar_uuid7,
    )

    hotel_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("hoteis.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    data_inicio: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    data_fim: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    multiplicador: Mapped[Decimal] = mapped_column(
        Numeric(4, 2),
        nullable=False,
    )

    hotel: Mapped["Hotel"] = relationship(
        back_populates="tarifas_temporada",
    )