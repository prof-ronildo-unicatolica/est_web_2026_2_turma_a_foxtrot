"""seed initial hotel domain

Revision ID: 8b8b95e00e89
Revises: 80b903434166
Create Date: 2026-08-20
"""

import uuid
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from passlib.context import CryptContext


# revision identifiers, used by Alembic.
revision: str = "8b8b95e00e89"
down_revision: Union[str, None] = "80b903434166"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Configuração para gerar o hash da senha do administrador.
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def upgrade() -> None:
    """Insere os dados iniciais do domínio hoteleiro."""

    # ---------------------------------------------------------
    # IDs fixos do seed
    # ---------------------------------------------------------

    # Usuário administrador
    admin_id = uuid.UUID(
        "10000000-0000-0000-0000-000000000001"
    )

    # Cidades
    fortaleza_id = uuid.UUID(
        "20000000-0000-0000-0000-000000000001"
    )
    quixada_id = uuid.UUID(
        "20000000-0000-0000-0000-000000000002"
    )
    sobral_id = uuid.UUID(
        "20000000-0000-0000-0000-000000000003"
    )

    # Hotéis
    hotel_1_id = uuid.UUID(
        "30000000-0000-0000-0000-000000000001"
    )
    hotel_2_id = uuid.UUID(
        "30000000-0000-0000-0000-000000000002"
    )
    hotel_3_id = uuid.UUID(
        "30000000-0000-0000-0000-000000000003"
    )
    hotel_4_id = uuid.UUID(
        "30000000-0000-0000-0000-000000000004"
    )
    hotel_5_id = uuid.UUID(
        "30000000-0000-0000-0000-000000000005"
    )

    # ---------------------------------------------------------
    # Seed do administrador
    # ---------------------------------------------------------

    senha_hash = pwd_context.hash("admin123")

    op.execute(
        sa.text(
            """
            INSERT INTO usuarios
                (id, nome, email, senha_hash, is_admin)
            VALUES
                (:id, :nome, :email, :senha_hash, :is_admin)
            """
        ).bindparams(
            id=str(admin_id),
            nome="Administrador",
            email="admin@hotel.com",
            senha_hash=senha_hash,
            is_admin=True,
        )
    )

    # ---------------------------------------------------------
    # Seed das cidades
    # ---------------------------------------------------------

    cidades = [
        (
            fortaleza_id,
            "Fortaleza",
            "CE",
        ),
        (
            quixada_id,
            "Quixadá",
            "CE",
        ),
        (
            sobral_id,
            "Sobral",
            "CE",
        ),
    ]

    for cidade_id, nome, estado in cidades:
        op.execute(
            sa.text(
                """
                INSERT INTO cidades
                    (id, nome, estado)
                VALUES
                    (:id, :nome, :estado)
                """
            ).bindparams(
                id=str(cidade_id),
                nome=nome,
                estado=estado,
            )
        )

    # ---------------------------------------------------------
    # Seed dos hotéis
    # ---------------------------------------------------------

    hoteis = [
        (
            hotel_1_id,
            "Hotel Sertão",
            1,
            "Rua Principal, 100",
            quixada_id,
        ),
        (
            hotel_2_id,
            "Hotel Central",
            2,
            "Avenida Centro, 200",
            sobral_id,
        ),
        (
            hotel_3_id,
            "Hotel Executivo",
            3,
            "Avenida Beira Mar, 300",
            fortaleza_id,
        ),
        (
            hotel_4_id,
            "Hotel Premium",
            4,
            "Avenida Dom Luís, 400",
            fortaleza_id,
        ),
        (
            hotel_5_id,
            "Hotel Atlântico",
            5,
            "Avenida Beira Mar, 500",
            fortaleza_id,
        ),
    ]

    for hotel_id, nome, estrelas, endereco, cidade_id in hoteis:
        op.execute(
            sa.text(
                """
                INSERT INTO hoteis
                    (id, nome, estrelas, endereco, cidade_id)
                VALUES
                    (:id, :nome, :estrelas, :endereco, :cidade_id)
                """
            ).bindparams(
                id=str(hotel_id),
                nome=nome,
                estrelas=estrelas,
                endereco=endereco,
                cidade_id=str(cidade_id),
            )
        )


def downgrade() -> None:
    """Remove somente os dados inseridos por esta migration."""

    # ---------------------------------------------------------
    # Remove os hotéis primeiro, pois possuem FK para cidades.
    # ---------------------------------------------------------

    op.execute(
        sa.text(
            """
            DELETE FROM hoteis
            WHERE id IN (
                '30000000-0000-0000-0000-000000000001',
                '30000000-0000-0000-0000-000000000002',
                '30000000-0000-0000-0000-000000000003',
                '30000000-0000-0000-0000-000000000004',
                '30000000-0000-0000-0000-000000000005'
            )
            """
        )
    )

    # ---------------------------------------------------------
    # Remove as cidades criadas pelo seed.
    # ---------------------------------------------------------

    op.execute(
        sa.text(
            """
            DELETE FROM cidades
            WHERE id IN (
                '20000000-0000-0000-0000-000000000001',
                '20000000-0000-0000-0000-000000000002',
                '20000000-0000-0000-0000-000000000003'
            )
            """
        )
    )

    # ---------------------------------------------------------
    # Remove o administrador criado pelo seed.
    # ---------------------------------------------------------

    op.execute(
        sa.text(
            """
            DELETE FROM usuarios
            WHERE id = '10000000-0000-0000-0000-000000000001'
            """
        )
    )