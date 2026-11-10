
"""Corrige estrelas e adiciona quartos de demonstracao.

Revision ID: b71eac90d3f8
Revises: e04df5867194
"""

import sqlalchemy as sa
from alembic import op

revision = "b71eac90d3f8"
down_revision = "e04df5867194"
branch_labels = None
depends_on = None


# Categorias originais dos hoteis do seed.
CATEGORIAS = {
    "30000000-0000-0000-0000-000000000002": 2,
    "30000000-0000-0000-0000-000000000003": 3,
    "30000000-0000-0000-0000-000000000004": 4,
    "30000000-0000-0000-0000-000000000005": 5,
}

# Hotel, numero, tipo, diaria, adultos, criancas.
QUARTOS = [
    (1, "101", "Economico", "140.00", 2, 0),
    (1, "102", "Familia", "190.00", 2, 2),
    (2, "201", "Standard", "220.00", 2, 1),
    (2, "202", "Superior", "290.00", 3, 1),
    (3, "301", "Executivo", "360.00", 2, 0),
    (3, "302", "Triplo", "440.00", 3, 1),
    (4, "401", "Luxo", "590.00", 2, 1),
    (4, "402", "Suite Premium", "760.00", 2, 2),
    (5, "501", "Vista Mar", "920.00", 2, 1),
    (5, "502", "Suite Master", "1250.00", 4, 2),
]


def hotel_id(numero):
    return f"30000000-0000-0000-0000-{numero:012d}"


def quarto_id(numero):
    return f"40000000-0000-0000-0000-{numero:012d}"


def upgrade():
    conexao = op.get_bind()

    # Corrige apenas categorias ainda incorretas.
    for identificador, estrelas in CATEGORIAS.items():
        conexao.execute(
            sa.text("""
                UPDATE hoteis
                SET categoria_estrelas = :estrelas
                WHERE id = CAST(:id AS UUID)
                  AND categoria_estrelas = 1
            """),
            {"id": identificador, "estrelas": estrelas},
        )

    # Adiciona os quartos sem duplicar numeros existentes.
    for indice, quarto in enumerate(QUARTOS, start=1):
        hotel, numero, tipo, diaria, adultos, criancas = quarto

        conexao.execute(
            sa.text("""
                INSERT INTO quartos (
                    id, hotel_id, numero, tipo,
                    preco_diaria, max_adultos, max_criancas
                )
                SELECT
                    CAST(:id AS UUID),
                    CAST(:hotel_id AS UUID),
                    :numero,
                    :tipo,
                    :diaria,
                    :adultos,
                    :criancas
                WHERE EXISTS (
                    SELECT 1 FROM hoteis
                    WHERE id = CAST(:hotel_id AS UUID)
                )
                AND NOT EXISTS (
                    SELECT 1 FROM quartos
                    WHERE hotel_id = CAST(:hotel_id AS UUID)
                      AND numero = :numero
                )
                ON CONFLICT (id) DO NOTHING
            """),
            {
                "id": quarto_id(indice),
                "hotel_id": hotel_id(hotel),
                "numero": numero,
                "tipo": tipo,
                "diaria": diaria,
                "adultos": adultos,
                "criancas": criancas,
            },
        )


def downgrade():
    conexao = op.get_bind()

    # Nao remove quartos que ja possuem reservas.
    for indice in range(1, len(QUARTOS) + 1):
        possui_reserva = conexao.execute(
            sa.text("""
                SELECT EXISTS (
                    SELECT 1 FROM reservas
                    WHERE quarto_id = CAST(:id AS UUID)
                )
            """),
            {"id": quarto_id(indice)},
        ).scalar()

        if possui_reserva:
            raise RuntimeError(
                "Nao e seguro reverter: existem reservas "
                "associadas aos quartos demonstrativos."
            )

    for indice, quarto in enumerate(QUARTOS, start=1):
        hotel, numero, *_ = quarto

        conexao.execute(
            sa.text("""
                DELETE FROM quartos
                WHERE id = CAST(:id AS UUID)
                  AND hotel_id = CAST(:hotel_id AS UUID)
                  AND numero = :numero
            """),
            {
                "id": quarto_id(indice),
                "hotel_id": hotel_id(hotel),
                "numero": numero,
            },
        )

    for identificador, estrelas in CATEGORIAS.items():
        conexao.execute(
            sa.text("""
                UPDATE hoteis
                SET categoria_estrelas = 1
                WHERE id = CAST(:id AS UUID)
                  AND categoria_estrelas = :estrelas
            """),
            {"id": identificador, "estrelas": estrelas},
        )
