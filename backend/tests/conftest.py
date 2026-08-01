import pytest
from app.config import Settings
from app.models import (  # noqa: F401  (registra los modelos en el metadata)
    AddOn,
    AppSettings,
    Category,
    Product,
    ProductAddOn,
)
from app.services import (
    AddOnService,
    AuthService,
    CategoryService,
    ProductService,
    SettingsService,
    UploadService,
)
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine


@pytest.fixture()
def db_engine():
    """Engine SQLite en memoria, aislado por test."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture()
def db_session(db_engine):
    """Sesión aislada por test con la base vacía ya creada."""
    with Session(db_engine) as session:
        yield session


@pytest.fixture()
def settings() -> Settings:
    """Configuración controlada para tests (secret fijo, tiempos cortos)."""
    return Settings(
        database_url="sqlite://",
        jwt_secret="test-secret",
        admin_username="admin",
        admin_password="admin123",
        access_token_expire_minutes=30,
    )


@pytest.fixture()
def auth_service(settings) -> AuthService:
    return AuthService(settings=settings)


@pytest.fixture()
def category_service(db_session) -> CategoryService:
    return CategoryService(session=db_session)


@pytest.fixture()
def product_service(db_session) -> ProductService:
    return ProductService(session=db_session)


@pytest.fixture()
def addon_service(db_session) -> AddOnService:
    return AddOnService(session=db_session)


@pytest.fixture()
def settings_service(db_session) -> SettingsService:
    return SettingsService(session=db_session)


@pytest.fixture()
def upload_service(settings) -> UploadService:
    return UploadService(settings=settings)


@pytest.fixture()
def a_category(db_session) -> Category:
    """Categoría base persistida para tests de productos."""
    cat = Category(name="Parrilla", order=1)
    db_session.add(cat)
    db_session.commit()
    db_session.refresh(cat)
    return cat


@pytest.fixture()
def an_addon(db_session) -> AddOn:
    """Adicional base persistido para tests de productos."""
    addon = AddOn(name="Queso extra", default_price=1.50)
    db_session.add(addon)
    db_session.commit()
    db_session.refresh(addon)
    return addon
