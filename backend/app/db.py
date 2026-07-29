import os
from sqlmodel import create_engine, SQLModel, Session

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://menu_user:menu_pass@localhost:5432/menu_db",
)

engine = create_engine(DATABASE_URL, echo=False)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
