from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db import get_session
from app.models.app_settings import AppSettings
from app.models.app_settings import MenuLayout
from app.routers.auth import require_auth
from app.schemas import SettingsOut, SettingsUpdate

router = APIRouter(prefix="/settings", tags=["settings"])

SETTINGS_ID = 1


def get_settings(session: Session) -> AppSettings:
    settings = session.get(AppSettings, SETTINGS_ID)
    if not settings:
        settings = AppSettings(id=SETTINGS_ID, layout=MenuLayout.GRID)
        session.add(settings)
        session.commit()
        session.refresh(settings)
    return settings


@router.get("", response_model=SettingsOut)
def read_settings(session: Session = Depends(get_session)):
    settings = get_settings(session)
    return SettingsOut(layout=settings.layout)


@router.put("", response_model=SettingsOut)
def update_settings(
    data: SettingsUpdate,
    session: Session = Depends(get_session),
    _: str = Depends(require_auth),
):
    settings = get_settings(session)
    settings.layout = data.layout
    session.add(settings)
    session.commit()
    session.refresh(settings)
    return SettingsOut(layout=settings.layout)
