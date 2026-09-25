from uuid import UUID

from sqlalchemy.orm import Session

from app.models.quarto import Quarto


class QuartoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        hotel_id: UUID,
        numero: str,
        tipo: str,
        preco_diaria: float,
        max_adultos: int,
        max_criancas: int,
    ) -> Quarto:
        quarto = Quarto(
            hotel_id=hotel_id,
            numero=numero,
            tipo=tipo,
            preco_diaria=preco_diaria,
            max_adultos=max_adultos,
            max_criancas=max_criancas,
        )

        self.db.add(quarto)
        self.db.commit()
        self.db.refresh(quarto)

        return quarto

    def list_by_hotel(self, hotel_id: UUID) -> list[Quarto]:
        return (
            self.db.query(Quarto)
            .filter(Quarto.hotel_id == hotel_id)
            .order_by(Quarto.numero)
            .all()
        )

    def get_by_id(self, quarto_id: UUID) -> Quarto | None:
        return (
            self.db.query(Quarto)
            .filter(Quarto.id == quarto_id)
            .first()
        )

    def update(
        self,
        quarto: Quarto,
        numero: str,
        tipo: str,
        preco_diaria: float,
        max_adultos: int,
        max_criancas: int,
    ) -> Quarto:
        quarto.numero = numero
        quarto.tipo = tipo
        quarto.preco_diaria = preco_diaria
        quarto.max_adultos = max_adultos
        quarto.max_criancas = max_criancas

        self.db.commit()
        self.db.refresh(quarto)

        return quarto

    def delete(self, quarto: Quarto) -> None:
        self.db.delete(quarto)
        self.db.commit()