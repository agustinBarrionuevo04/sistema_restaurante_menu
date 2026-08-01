from fastapi import Depends
from sqlmodel import Session

from app.config import Settings, get_settings
from app.db import get_session
from app.services import (
    AddOnService,
    CategoryService,
    ProductService,
    SettingsService,
    UploadService,
)


def get_category_service(session: Session = Depends(get_session)) -> CategoryService:
    return CategoryService(session=session)


def get_product_service(session: Session = Depends(get_session)) -> ProductService:
    return ProductService(session=session)


def get_addon_service(session: Session = Depends(get_session)) -> AddOnService:
    return AddOnService(session=session)


def get_settings_service(session: Session = Depends(get_session)) -> SettingsService:
    return SettingsService(session=session)


def get_upload_service(settings: Settings = Depends(get_settings)) -> UploadService:
    return UploadService(settings=settings)
