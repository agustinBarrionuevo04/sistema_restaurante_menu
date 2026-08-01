from fastapi import APIRouter, Depends

from app.deps import get_settings_service
from app.schemas import SettingsOut, SettingsUpdate
from app.services import SettingsService
from app.services.auth_service import require_auth

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("", response_model=SettingsOut)
def read_settings(service: SettingsService = Depends(get_settings_service)):
    """Devuelve la configuración pública de la carta (layout)."""
    return SettingsOut(layout=service.get())


@router.put("", response_model=SettingsOut)
def update_settings(
    data: SettingsUpdate,
    _: str = Depends(require_auth),
    service: SettingsService = Depends(get_settings_service),
):
    """Actualiza la configuración de la carta (requiere autenticación)."""
    return SettingsOut(layout=service.update(data.layout))
