from dataclasses import dataclass

from app.models.app_settings import AppSettings, MenuLayout
from app.services.base import BaseService

SETTINGS_ID = 1


@dataclass
class SettingsService(BaseService):
    """Servicio de configuración global (layout de la carta).

    La configuración se guarda como un único registro con id fijo (singleton).
    """

    def _get_or_create(self) -> AppSettings:
        settings = self.session.get(AppSettings, SETTINGS_ID)
        if settings is None:
            settings = AppSettings(id=SETTINGS_ID, layout=MenuLayout.GRID)
            self.commit_refresh(settings)
        return settings

    def get(self) -> MenuLayout:
        """Devuelve el layout configurado (grid por defecto si no existe)."""
        return self._get_or_create().layout

    def update(self, layout: MenuLayout) -> MenuLayout:
        """Actualiza el layout de la carta y persiste el cambio."""
        settings = self._get_or_create()
        settings.layout = layout
        self.session.add(settings)
        self.session.commit()
        self.session.refresh(settings)
        return settings.layout
