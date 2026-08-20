from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.uuid_utils import gerar_uuid7
from app.models.base import Base


if TYPE_CHECKING:
    from app.models.cidade import Cidade
    
class Hotel(Base):
    __tablename__ = "hoteis"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=gerar_uuid7,
    )

    nome: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    estrelas: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    endereco: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    cidade_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("cidades.id", ondelete="CASCADE"),
        nullable=False,
    )

    cidade: Mapped["Cidade"] = relationship(
        back_populates="hoteis",
    )