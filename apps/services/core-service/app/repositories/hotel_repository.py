from typing import List

from sqlalchemy.orm import Session, joinedload

from app.models.cidade import Cidade
from app.models.hotel import Hotel


class CidadeRepository:
    """Acesso ao banco para a entidade Cidade. Sem regra de negocio aqui."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, nome: str) -> Cidade:
        cidade = Cidade(nome=nome)
        self.db.add(cidade)
        self.db.commit()
        self.db.refresh(cidade)
        return cidade

    def list(self) -> List[Cidade]:
        return self.db.query(Cidade).order_by(Cidade.nome).all()

    def get_by_id(self, cidade_id) -> Cidade | None:
        """Devolve None quando a cidade nao existe."""

        return self.db.query(Cidade).filter(Cidade.id == cidade_id).first()

    def get_by_nome(self, nome: str) -> Cidade | None:
        return self.db.query(Cidade).filter(Cidade.nome == nome).first()


class HotelRepository:
    """Acesso ao banco para a entidade Hotel."""

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        nome: str,
        estrelas: int,
        endereco: str,
        cidade_id,
    ) -> Hotel:
        hotel = Hotel(
            nome=nome,
            estrelas=estrelas,
            endereco=endereco,
            cidade_id=cidade_id,
        )
        self.db.add(hotel)
        self.db.commit()
        self.db.refresh(hotel)
        return hotel

    def list(self) -> List[Hotel]:
        return (
            self.db.query(Hotel)
            .options(joinedload(Hotel.cidade))
            .order_by(Hotel.nome)
            .all()
        )

    def list_by_cidade(self, cidade_id) -> List[Hotel]:
        return (
            self.db.query(Hotel)
            .options(joinedload(Hotel.cidade))
            .filter(Hotel.cidade_id == cidade_id)
            .order_by(Hotel.nome)
            .all()
        )

    def get_by_id(self, hotel_id) -> Hotel | None:
        return (
            self.db.query(Hotel)
            .options(joinedload(Hotel.cidade))
            .filter(Hotel.id == hotel_id)
            .first()
        )