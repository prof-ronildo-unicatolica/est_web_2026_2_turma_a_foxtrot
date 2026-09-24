from sqlalchemy.orm import Session

from app.models.comodidade import Comodidade
from app.repositories.comodidade_repository import ComodidadeRepository


class ComodidadeJaExisteError(Exception):
    pass


class ComodidadeService:
    def __init__(self, db: Session):
        self.repository = ComodidadeRepository(db)

    def criar(self, nome: str) -> Comodidade:
        nome = nome.strip()

        if self.repository.get_by_nome(nome):
            raise ComodidadeJaExisteError(
                f"Ja existe uma comodidade chamada '{nome}'."
            )

        return self.repository.create(nome=nome)

    def listar(self) -> list[Comodidade]:
        return self.repository.list()