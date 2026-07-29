import uuid
from decimal import Decimal
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class ProductAddOn(SQLModel, table=True):
    __tablename__ = "product_addons"

    product_id: uuid.UUID = Field(foreign_key="products.id", primary_key=True)
    addon_id: uuid.UUID = Field(foreign_key="addons.id", primary_key=True)
    price_override: Optional[Decimal] = Field(default=None, max_digits=10, decimal_places=2)

    product: "Product" = Relationship(back_populates="product_addons")
    addon: "AddOn" = Relationship(back_populates="product_addons")
