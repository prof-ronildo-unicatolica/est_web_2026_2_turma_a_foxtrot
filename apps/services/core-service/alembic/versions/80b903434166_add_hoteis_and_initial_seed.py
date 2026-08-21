"""add hoteis and initial seed

Revision ID: 80b903434166
Revises: e467949768bc
Create Date: 2026-08-20 22:58:16.336824

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "80b903434166"
down_revision: Union[str, None] = "e467949768bc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "hoteis",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("nome", sa.String(length=150), nullable=False),
        sa.Column("estrelas", sa.Integer(), nullable=False),
        sa.Column("endereco", sa.String(length=255), nullable=False),
        sa.Column("cidade_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["cidade_id"],
            ["cidades.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("hoteis")