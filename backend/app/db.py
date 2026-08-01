from sqlmodel import Session, create_engine

from app.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.database_url,
    echo=False,
    connect_args={"check_same_thread": False}
    if settings.database_url.startswith("sqlite")
    else {},
)


def get_session():
    """Dependencia que provee una sesión de base de datos por petición."""
    with Session(engine) as session:
        yield session
