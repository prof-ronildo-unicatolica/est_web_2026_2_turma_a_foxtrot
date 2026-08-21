import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import get_db
from app.main import app

# Base principal
from app.models.base import Base

# Importar todos os models para registrá-los no Base.metadata
from app.models.tutorial import (
    Professor,
    ProfessorDetail,
    Disciplina,
    Stack,
    Tecnologia,
    Linguagem,
)
from app.models.usuario import Usuario
from app.models.cidade import Cidade
from app.models.hotel import Hotel

from sqlalchemy.orm import configure_mappers

print("MODELS CARREGADOS NO CONFTEST:")
print(sorted(Base.registry._class_registry.keys()))

configure_mappers()

print("MAPPERS CONFIGURADOS NO CONFTEST")

# Banco SQLite em arquivo temporário para os testes
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    # Desativamos raise_server_exceptions para validar retornos de erro 500
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c

    app.dependency_overrides.clear()