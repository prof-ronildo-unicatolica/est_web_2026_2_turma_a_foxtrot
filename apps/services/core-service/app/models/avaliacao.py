from uuid import UUID

from sqlalchemy import CheckConstraint, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.uuid_utils import gerar_uuid7
from app.models.base import Base


class Avaliacao(Base):
    __tablename__ = "avaliacoes"

    __table_args__ = (
        UniqueConstraint("reserva_id", name="uq_avaliacoes_reserva_id"),
        CheckConstraint("nota >= 1 AND nota <= 5", name="ck_avaliacoes_nota"),
    )

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=gerar_uuid7,
    )

    reserva_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("reservas.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    hotel_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("hoteis.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    nota: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    comentario: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
