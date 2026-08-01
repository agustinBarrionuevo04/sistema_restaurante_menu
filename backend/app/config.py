from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración central de la aplicación, leída desde variables de entorno y .env.

    Todos los valores que antes se leían dispersos (db, jwt, admin, r2, cors, uploads)
    quedan centralizados aquí y son inyectables por dependencia.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = "sqlite:///./menu.db"

    jwt_secret: str = "dev-secret-change-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

    admin_username: str = "admin"
    admin_password: str = "admin123"

    r2_access_key: str = ""
    r2_secret_key: str = ""
    r2_endpoint: str = ""
    r2_bucket: str = ""
    r2_public_url: str = ""

    public_base_url: str = "http://localhost:8000"

    uploads_dir: str = "static/products"

    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://localhost:5174",
    ]


@lru_cache
def get_settings() -> Settings:
    """Proveedor cacheado de Settings, útil para inyección por dependencia."""
    return Settings()
