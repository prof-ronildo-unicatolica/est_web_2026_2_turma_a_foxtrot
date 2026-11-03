
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from app.api.v1.auth import router as auth_router
from app.api.v1.cidades import router as cidades_router
from app.api.v1.comodidades import router as comodidades_router
from app.api.v1.health import router as health_router
from app.api.v1.hoteis import router as hoteis_router
from app.api.v1.quartos import router as quartos_router
from app.api.v1.reservas import router as reservas_router
from app.api.v1.sobre import router as sobre_router
from app.core.config import settings
from app.core.database import SessionLocal
from app.core.seed_mongo import seed_mongo_users
from app.models.hotel import Hotel
from app.services.catalogo_hotel_service import CatalogoHotelService


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Cria uma nova conexão MongoDB para esta inicialização.
    mongo_client = AsyncIOMotorClient(settings.MONGODB_URL)
    app.state.mongo_db = mongo_client[settings.MONGODB_DB]

    try:
        # Inicializa os dados do MongoDB.
        await seed_mongo_users(app.state.mongo_db)

        # Sincroniza os hotéis do PostgreSQL com o MongoDB.
        db = SessionLocal()

        try:
            hoteis = db.query(Hotel.id).all()
            catalogo = CatalogoHotelService(
                db,
                app.state.mongo_db,
            )

            for (hotel_id,) in hoteis:
                await catalogo.sincronizar_hotel(hotel_id)

            print(
                f"Catálogo MongoDB sincronizado: {len(hoteis)} hotéis",
                flush=True,
            )

        finally:
            db.close()

        yield

    finally:
        # Encerra a conexão junto com a aplicação.
        mongo_client.close()
        app.state.mongo_db = None


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# Configuração de CORS para acesso do frontend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix=settings.API_V1_STR)
app.include_router(sobre_router, prefix=settings.API_V1_STR)
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(cidades_router, prefix=settings.API_V1_STR)
app.include_router(hoteis_router, prefix=settings.API_V1_STR)
app.include_router(comodidades_router, prefix=settings.API_V1_STR)
app.include_router(quartos_router, prefix=settings.API_V1_STR)
app.include_router(reservas_router, prefix=settings.API_V1_STR)


@app.get("/")
def read_root():
    return {
        "message": "Bem-vindo ao Core Service do Sistema de Reservas!"
    }
