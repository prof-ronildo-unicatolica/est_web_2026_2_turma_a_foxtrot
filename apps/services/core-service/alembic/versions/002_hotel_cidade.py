"""ajusta tabelas cidades e hoteis para o modelo 1:N

Revision ID: 002
Revises: 8b8b95e00e89
Create Date: 2026-09-08

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "002"
down_revision: Union[str, None] = "8b8b95e00e89"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Cidade agora possui somente id e nome.
    op.drop_column("cidades", "estado")

    # O nome da cidade deve ser único.
    op.create_unique_constraint(
        "uq_cidades_nome",
        "cidades",
        ["nome"],
    )

    # Hotel agora possui somente id, nome e cidade_id.
    op.drop_column("hoteis", "estrelas")
    op.drop_column("hoteis", "endereco")

    # Alinha o tamanho do nome com o model atual.
    op.alter_column(
        "hoteis",
        "nome",
        existing_type=sa.String(length=150),
        type_=sa.String(length=100),
        existing_nullable=False,
    )

    # Índice utilizado nas consultas de hotéis por cidade.
    op.create_index(
        "ix_hoteis_cidade_id",
        "hoteis",
        ["cidade_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_hoteis_cidade_id",
        table_name="hoteis",
    )

    op.alter_column(
        "hoteis",
        "nome",
        existing_type=sa.String(length=100),
        type_=sa.String(length=150),
        existing_nullable=False,
    )

    op.add_column(
        "hoteis",
        sa.Column(
            "endereco",
            sa.String(length=255),
            nullable=False,
            server_default="N/A",
        ),
    )

    op.add_column(
        "hoteis",
        sa.Column(
            "estrelas",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )

    op.drop_constraint(
        "uq_cidades_nome",
        "cidades",
        type_="unique",
    )

    op.add_column(
        "cidades",
        sa.Column(
            "estado",
            sa.String(length=100),
            nullable=False,
            server_default="CE",
        ),
    )

    # Remove os defaults usados somente para restaurar registros existentes.
    op.alter_column(
        "hoteis",
        "endereco",
        server_default=None,
    )
    op.alter_column(
        "hoteis",
        "estrelas",
        server_default=None,
    )
    op.alter_column(
        "cidades",
        "estado",
        server_default=None,
    )