from uuid import UUID

from sqlalchemy.orm import Session

from app.models.quarto import Quarto
from app.repositories.hotel_repository import HotelRepository
from app.repositories.quarto_repository import QuartoRepository


class HotelNaoEncontradoError(Exception):
    pass


class QuartoNaoEncontradoError(Exception):
    pass


class QuartoService:
    def __init__(self, db: Session):
        self.repository = QuartoRepository(db)
        self.hoteis = HotelRepository(db)

    def criar(
        self,
        hotel_id: UUID,
        numero: str,
        tipo: str,
        preco_diaria: float,
        max_adultos: int,
        max_criancas: int,
    ) -> Quarto:
        hotel = self.hoteis.get_by_id(hotel_id)

        if not hotel:
            raise HotelNaoEncontradoError(
                f"Não existe hotel com id '{hotel_id}'."
            )

        return self.repository.create(
            hotel_id=hotel_id,
            numero=numero.strip(),
            tipo=tipo.strip(),
            preco_diaria=preco_diaria,
            max_adultos=max_adultos,
            max_criancas=max_criancas,
        )

    def listar_por_hotel(self, hotel_id: UUID) -> list[Quarto]:
        hotel = self.hoteis.get_by_id(hotel_id)

        if not hotel:
            raise HotelNaoEncontradoError(
                f"Não existe hotel com id '{hotel_id}'."
            )

        return self.repository.list_by_hotel(hotel_id)

    def buscar(self, quarto_id: UUID) -> Quarto:
        quarto = self.repository.get_by_id(quarto_id)

        if not quarto:
            raise QuartoNaoEncontradoError(
                f"Não existe quarto com id '{quarto_id}'."
            )

        return quarto

    def atualizar(
        self,
        quarto_id: UUID,
        numero: str,
        tipo: str,
        preco_diaria: float,
        max_adultos: int,
        max_criancas: int,
    ) -> Quarto:
        quarto = self.buscar(quarto_id)

        return self.repository.update(
            quarto=quarto,
            numero=numero.strip(),
            tipo=tipo.strip(),
            preco_diaria=preco_diaria,
            max_adultos=max_adultos,
            max_criancas=max_criancas,
        )

    def excluir(self, quarto_id: UUID) -> None:
        quarto = self.buscar(quarto_id)
        self.repository.delete(quarto)