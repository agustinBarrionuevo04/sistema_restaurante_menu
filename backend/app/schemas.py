import uuid
from decimal import Decimal

from pydantic import BaseModel

from app.models.app_settings import MenuLayout
from app.models.product import ProductStatus


class CategoryCreate(BaseModel):
    name: str
    order: int = 0


class CategoryUpdate(BaseModel):
    name: str | None = None
    order: int | None = None


class CategoryOut(BaseModel):
    id: uuid.UUID
    name: str
    order: int

    model_config = {"from_attributes": True}


class ProductCreate(BaseModel):
    category_id: uuid.UUID
    name: str
    description: str = ""
    base_price: Decimal
    image_url: str | None = None
    status: ProductStatus = ProductStatus.ACTIVE


class ProductUpdate(BaseModel):
    category_id: uuid.UUID | None = None
    name: str | None = None
    description: str | None = None
    base_price: Decimal | None = None
    image_url: str | None = None
    status: ProductStatus | None = None


class AddOnOut(BaseModel):
    id: uuid.UUID
    name: str
    default_price: Decimal

    model_config = {"from_attributes": True}


class ProductAddOnOut(BaseModel):
    addon: AddOnOut
    price_override: Decimal | None = None

    model_config = {"from_attributes": True}


class ProductOut(BaseModel):
    id: uuid.UUID
    category_id: uuid.UUID
    name: str
    description: str
    base_price: Decimal
    image_url: str | None = None
    status: ProductStatus
    addons: list[ProductAddOnOut] = []

    model_config = {"from_attributes": True}


class AddOnCreate(BaseModel):
    name: str
    default_price: Decimal


class AddOnUpdate(BaseModel):
    name: str | None = None
    default_price: Decimal | None = None


class ProductAddOnCreate(BaseModel):
    addon_id: uuid.UUID
    price_override: Decimal | None = None


class PresignRequest(BaseModel):
    filename: str
    content_type: str = "image/jpeg"


class PresignResponse(BaseModel):
    upload_url: str
    public_url: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class SettingsOut(BaseModel):
    layout: MenuLayout


class SettingsUpdate(BaseModel):
    layout: MenuLayout
