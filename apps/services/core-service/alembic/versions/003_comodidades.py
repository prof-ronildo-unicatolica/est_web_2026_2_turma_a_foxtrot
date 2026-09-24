"""adiciona comodidades e associacao com hoteis

Revision ID: 003
Revises: 002
Create Date: 2026-09-19
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ---------------------------------------------------------
    # Tabela de comodidades
    # ---------------------------------------------------------

    op.create_table(
        "comodidades",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "nome",
            sa.String(length=100),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("nome"),
    )

    # ---------------------------------------------------------
    # Relação N:N entre hotéis e comodidades
    # ---------------------------------------------------------

    op.create_table(
        "hotel_comodidades",
        sa.Column(
            "hotel_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "comodidade_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["hotel_id"],
            ["hoteis.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["comodidade_id"],
            ["comodidades.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "hotel_id",
            "comodidade_id",
        ),
    )


def downgrade() -> None:
    op.drop_table("hotel_comodidades")
    op.drop_table("comodidades")