"""cria tabela de quartos

Revision ID: 005
Revises: 004
Create Date: 2026-09-24
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = "005"
down_revision: Union[str, None] = "004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "quartos",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "hotel_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "numero",
            sa.String(length=10),
            nullable=False,
        ),
        sa.Column(
            "tipo",
            sa.String(length=50),
            nullable=False,
        ),
        sa.Column(
            "preco_diaria",
            sa.Numeric(precision=10, scale=2),
            nullable=False,
        ),
        sa.Column(
            "max_adultos",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "max_criancas",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
        sa.ForeignKeyConstraint(
            ["hotel_id"],
            ["hoteis.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.CheckConstraint(
            "preco_diaria >= 0",
            name="ck_quartos_preco_diaria",
        ),
        sa.CheckConstraint(
            "max_adultos >= 1",
            name="ck_quartos_max_adultos",
        ),
        sa.CheckConstraint(
            "max_criancas >= 0",
            name="ck_quartos_max_criancas",
        ),
    )

    op.create_index(
        "ix_quartos_hotel_id",
        "quartos",
        ["hotel_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_quartos_hotel_id",
        table_name="quartos",
    )
    op.drop_table("quartos")