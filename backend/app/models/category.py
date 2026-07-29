import uuid

from sqlmodel import SQLModel, Field, Relationship


class Category(SQLModel, table=True):
    __tablename__ = "categories"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=255)
    order: int = Field(default=0)

    products: list["Product"] = Relationship(back_populates="category")
