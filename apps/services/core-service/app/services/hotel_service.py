
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.avaliacao import Avaliacao
from app.models.cidade import Cidade
from app.models.hotel import Hotel
from app.repositories.comodidade_repository import ComodidadeRepository
from app.repositories.hotel_repository import CidadeRepository, HotelRepository


# --- Excecoes de dominio -----------------------------------------------------


class RegraDeNegocioError(Exception):
    """Base de todas as excecoes de negocio deste modulo."""


class CidadeJaExisteError(RegraDeNegocioError):
    pass


class CidadeNaoEncontradaError(RegraDeNegocioError):
    pass


class HotelNaoEncontradoError(RegraDeNegocioError):
    pass


class ComodidadeNaoEncontradaError(RegraDeNegocioError):
    pass


# --- Services ----------------------------------------------------------------


class CidadeService:
    def __init__(self, db: Session):
        self.repository = CidadeRepository(db)

    def criar(
        self,
        nome: str,
        limite_territorial: dict | None = None,
    ) -> Cidade:
        nome = nome.strip()

        if self.repository.get_by_nome(nome):
            raise CidadeJaExisteError(
                f"Ja existe uma cidade chamada '{nome}'."
            )

        return self.repository.create(
            nome=nome,
            limite_territorial=limite_territorial,
        )

    def listar(self) -> list[Cidade]:
        return self.repository.list()


class HotelService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = HotelRepository(db)
        self.cidades = CidadeRepository(db)
        self.comodidades = ComodidadeRepository(db)

    def criar(
        self,
        nome: str,
        cidade_id,
        categoria_estrelas: int,
    ) -> Hotel:
        nome = nome.strip()

        if not self.cidades.get_by_id(cidade_id):
            raise CidadeNaoEncontradaError(
                f"Nao existe cidade com id '{cidade_id}'."
            )

        return self.repository.create(
            nome=nome,
            cidade_id=cidade_id,
            categoria_estrelas=categoria_estrelas,
        )

    def adicionar_comodidade(
        self,
        hotel_id,
        comodidade_id,
    ) -> Hotel:
        hotel = self.repository.get_by_id(hotel_id)

        if not hotel:
            raise HotelNaoEncontradoError(
                f"Nao existe hotel com id '{hotel_id}'."
            )

        comodidade = self.comodidades.get_by_id(comodidade_id)

        if not comodidade:
            raise ComodidadeNaoEncontradaError(
                f"Nao existe comodidade com id '{comodidade_id}'."
            )

        return self.repository.adicionar_comodidade(
            hotel=hotel,
            comodidade=comodidade,
        )

    def _anexar_estatisticas_avaliacoes(
        self,
        hoteis: list[Hotel],
    ) -> list[Hotel]:
        if not hoteis:
            return hoteis

        hotel_ids = [hotel.id for hotel in hoteis]

        resultados = (
            self.db.query(
                Avaliacao.hotel_id,
                func.avg(Avaliacao.nota),
                func.count(Avaliacao.id),
            )
            .filter(Avaliacao.hotel_id.in_(hotel_ids))
            .group_by(Avaliacao.hotel_id)
            .all()
        )

        estatisticas = {
            hotel_id: (float(media), quantidade)
            for hotel_id, media, quantidade in resultados
        }

        for hotel in hoteis:
            media, quantidade = estatisticas.get(
                hotel.id,
                (0.0, 0),
            )
            hotel.media_avaliacoes = round(media, 2)
            hotel.quantidade_avaliacoes = quantidade

        return hoteis

    def obter_detalhe(self, hotel_id) -> Hotel:
        hotel = self.repository.get_by_id(hotel_id)

        if not hotel:
            raise HotelNaoEncontradoError(
                f"Nao existe hotel com id '{hotel_id}'."
            )

        self._anexar_estatisticas_avaliacoes([hotel])
        return hotel

    def listar(self, cidade_id=None) -> list[Hotel]:
        if cidade_id is not None:
            if not self.cidades.get_by_id(cidade_id):
                raise CidadeNaoEncontradaError(
                    f"Nao existe cidade com id '{cidade_id}'."
                )

            hoteis = self.repository.list_by_cidade(cidade_id)
        else:
            hoteis = self.repository.list()

        return self._anexar_estatisticas_avaliacoes(hoteis)
