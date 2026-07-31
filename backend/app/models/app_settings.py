from enum import Enum

from sqlmodel import SQLModel, Field


class MenuLayout(str, Enum):
    LIST = "list"
    GRID = "grid"
    CAROUSEL = "carousel"


class AppSettings(SQLModel, table=True):
    __tablename__ = "app_settings"

    id: int = Field(default=1, primary_key=True)
    layout: MenuLayout = Field(default=MenuLayout.GRID)
