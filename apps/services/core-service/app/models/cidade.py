from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.uuid_utils import gerar_uuid7
from app.models.base import Base


if TYPE_CHECKING:
    from app.models.hotel import Hotel


class Cidade(Base):
    __tablename__ = "cidades"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=gerar_uuid7,
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    estado: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    hoteis: Mapped[list["Hotel"]] = relationship(
        back_populates="cidade",
        cascade="all, delete-orphan",
    )