import uuid
from decimal import Decimal
from enum import StrEnum

from sqlmodel import Field, Relationship, SQLModel


class ProductStatus(StrEnum):
    ACTIVE = "active"
    SUSPENDED = "suspended"


class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    category_id: uuid.UUID = Field(foreign_key="categories.id")
    name: str = Field(max_length=255)
    description: str = Field(default="")
    base_price: Decimal = Field(max_digits=10, decimal_places=2)
    image_url: str | None = Field(default=None)
    status: ProductStatus = Field(default=ProductStatus.ACTIVE)

    category: "Category" = Relationship(back_populates="products")
    product_addons: list["ProductAddOn"] = Relationship(
        back_populates="product", cascade_delete=True
    )
