import uuid
from decimal import Decimal

from sqlmodel import SQLModel, Field, Relationship


class AddOn(SQLModel, table=True):
    __tablename__ = "addons"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=255)
    default_price: Decimal = Field(max_digits=10, decimal_places=2)

    product_addons: list["ProductAddOn"] = Relationship(back_populates="addon", cascade_delete=True)
