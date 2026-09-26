from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c4d6f489a921"
down_revision: Union[str, None] = "005"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "servicos_adicionais",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("nome", sa.String(length=100), nullable=False),
        sa.Column("preco", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.CheckConstraint(
            "preco >= 0",
            name="ck_servicos_adicionais_preco_nao_negativo",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "tarifas_temporada",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("hotel_id", sa.UUID(), nullable=False),
        sa.Column("nome", sa.String(length=100), nullable=False),
        sa.Column("data_inicio", sa.Date(), nullable=False),
        sa.Column("data_fim", sa.Date(), nullable=False),
        sa.Column(
            "multiplicador",
            sa.Numeric(precision=4, scale=2),
            nullable=False,
        ),
        sa.CheckConstraint(
            "data_fim >= data_inicio",
            name="ck_tarifas_temporada_periodo_valido",
        ),
        sa.CheckConstraint(
            "multiplicador > 0",
            name="ck_tarifas_temporada_multiplicador_positivo",
        ),
        sa.ForeignKeyConstraint(
            ["hotel_id"],
            ["hoteis.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_tarifas_temporada_hotel_id"),
        "tarifas_temporada",
        ["hotel_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_tarifas_temporada_hotel_id"),
        table_name="tarifas_temporada",
    )
    op.drop_table("tarifas_temporada")
    op.drop_table("servicos_adicionais")