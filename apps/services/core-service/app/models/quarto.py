from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.uuid_utils import gerar_uuid7
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.hotel import Hotel


class Quarto(Base):
    __tablename__ = "quartos"

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

    numero: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    tipo: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    preco_diaria: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    max_adultos: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    max_criancas: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )

    hotel: Mapped["Hotel"] = relationship(
        back_populates="quartos",
    )