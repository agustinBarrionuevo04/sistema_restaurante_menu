from enum import StrEnum

from sqlmodel import Field, SQLModel


class MenuLayout(StrEnum):
    LIST = "list"
    GRID = "grid"
    CAROUSEL = "carousel"


class AppSettings(SQLModel, table=True):
    __tablename__ = "app_settings"

    id: int = Field(default=1, primary_key=True)
    layout: MenuLayout = Field(default=MenuLayout.GRID)
