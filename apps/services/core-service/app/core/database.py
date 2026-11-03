
from fastapi import Request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# --- Configuração do PostgreSQL ---
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Conexão MongoDB gerenciada pela aplicação ---
def get_mongo_db(request: Request):
    return request.app.state.mongo_db
