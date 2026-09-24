from typing import List

from sqlalchemy.orm import Session

from app.models.comodidade import Comodidade


class ComodidadeRepository:
    """Acesso ao banco para a entidade Comodidade."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, nome: str) -> Comodidade:
        comodidade = Comodidade(nome=nome)
        self.db.add(comodidade)
        self.db.commit()
        self.db.refresh(comodidade)
        return comodidade

    def list(self) -> List[Comodidade]:
        return (
            self.db.query(Comodidade)
            .order_by(Comodidade.nome)
            .all()
        )

    def get_by_id(self, comodidade_id) -> Comodidade | None:
        return (
            self.db.query(Comodidade)
            .filter(Comodidade.id == comodidade_id)
            .first()
        )

    def get_by_nome(self, nome: str) -> Comodidade | None:
        return (
            self.db.query(Comodidade)
            .filter(Comodidade.nome == nome)
            .first()
        )