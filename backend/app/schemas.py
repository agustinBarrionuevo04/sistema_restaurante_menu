import uuid
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from app.models.product import ProductStatus
from app.models.app_settings import MenuLayout


class CategoryCreate(BaseModel):
    name: str
    order: int = 0


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    order: Optional[int] = None


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
    image_url: Optional[str] = None
    status: ProductStatus = ProductStatus.ACTIVE


class ProductUpdate(BaseModel):
    category_id: Optional[uuid.UUID] = None
    name: Optional[str] = None
    description: Optional[str] = None
    base_price: Optional[Decimal] = None
    image_url: Optional[str] = None
    status: Optional[ProductStatus] = None


class AddOnOut(BaseModel):
    id: uuid.UUID
    name: str
    default_price: Decimal

    model_config = {"from_attributes": True}


class ProductAddOnOut(BaseModel):
    addon: AddOnOut
    price_override: Optional[Decimal] = None

    model_config = {"from_attributes": True}


class ProductOut(BaseModel):
    id: uuid.UUID
    category_id: uuid.UUID
    name: str
    description: str
    base_price: Decimal
    image_url: Optional[str] = None
    status: ProductStatus
    addons: list[ProductAddOnOut] = []

    model_config = {"from_attributes": True}


class AddOnCreate(BaseModel):
    name: str
    default_price: Decimal


class AddOnUpdate(BaseModel):
    name: Optional[str] = None
    default_price: Optional[Decimal] = None


class ProductAddOnCreate(BaseModel):
    addon_id: uuid.UUID
    price_override: Optional[Decimal] = None


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
