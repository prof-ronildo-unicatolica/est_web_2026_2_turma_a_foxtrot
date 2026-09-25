from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.uuid_utils import gerar_uuid7
from app.models.base import Base
from app.models.cidade import Cidade
from app.models.quarto import Quarto

if TYPE_CHECKING:
    from app.models.comodidade import Comodidade


hotel_comodidades = Table(
    "hotel_comodidades",
    Base.metadata,
    Column(
        "hotel_id",
        PG_UUID(as_uuid=True),
        ForeignKey("hoteis.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "comodidade_id",
        PG_UUID(as_uuid=True),
        ForeignKey("comodidades.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Hotel(Base):
    __tablename__ = "hoteis"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=gerar_uuid7,
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    categoria_estrelas: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    cidade_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("cidades.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    cidade: Mapped["Cidade"] = relationship(
        back_populates="hoteis",
    )

    quartos: Mapped[list["Quarto"]] = relationship(
        back_populates="hotel",
        cascade="all, delete-orphan",
    )

    comodidades: Mapped[list["Comodidade"]] = relationship(
        secondary=hotel_comodidades,
        back_populates="hoteis",
    )