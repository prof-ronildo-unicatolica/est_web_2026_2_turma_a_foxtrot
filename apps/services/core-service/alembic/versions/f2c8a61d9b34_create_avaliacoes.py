
"""Cria a tabela de avaliacoes.

Revision ID: f2c8a61d9b34
Revises: b71eac90d3f8
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision = "f2c8a61d9b34"
down_revision = "b71eac90d3f8"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "avaliacoes",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "reserva_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "hotel_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "nota",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "comentario",
            sa.Text(),
            nullable=True,
        ),
        sa.CheckConstraint(
            "nota >= 1 AND nota <= 5",
            name="ck_avaliacoes_nota",
        ),
        sa.ForeignKeyConstraint(
            ["reserva_id"],
            ["reservas.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["hotel_id"],
            ["hoteis.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "reserva_id",
            name="uq_avaliacoes_reserva_id",
        ),
    )

    op.create_index(
        "ix_avaliacoes_reserva_id",
        "avaliacoes",
        ["reserva_id"],
    )

    op.create_index(
        "ix_avaliacoes_hotel_id",
        "avaliacoes",
        ["hotel_id"],
    )


def downgrade():
    op.drop_index(
        "ix_avaliacoes_hotel_id",
        table_name="avaliacoes",
    )

    op.drop_index(
        "ix_avaliacoes_reserva_id",
        table_name="avaliacoes",
    )

    op.drop_table("avaliacoes")
