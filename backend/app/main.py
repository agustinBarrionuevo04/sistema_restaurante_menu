import os
from contextlib import asynccontextmanager
from pathlib import Path

from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.routers import addons, auth, categories, products, settings, uploads

_ALEMBIC_INI = Path(__file__).resolve().parent.parent / "alembic.ini"


def run_migrations() -> None:
    """Aplica las migraciones de base de datos (alembic upgrade head)."""
    config = Config(str(_ALEMBIC_INI))
    config.set_main_option("script_location", str(_ALEMBIC_INI.parent / "alembic"))
    command.upgrade(config, "head")


def create_app(*, apply_migrations: bool = True) -> FastAPI:
    """Factory de la aplicación FastAPI.

    ``apply_migrations`` permite omitir las migraciones en entornos de prueba
    donde la base de datos se prepara con otro mecanismo (p. ej. create_all).
    """

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if apply_migrations:
            run_migrations()
        yield

    app_settings = get_settings()

    app = FastAPI(
        title="Carta Digital API",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(categories.router)
    app.include_router(products.router)
    app.include_router(addons.router)
    app.include_router(uploads.router)
    app.include_router(auth.router)
    app.include_router(settings.router)

    static_dir = os.path.join(os.path.dirname(__file__), "static")
    os.makedirs(static_dir, exist_ok=True)
    app.mount("/uploads/local", StaticFiles(directory=static_dir), name="static")

    @app.get("/health")
    def health():
        """Healthcheck de la API."""
        return {"status": "ok"}

    return app


app = create_app()
