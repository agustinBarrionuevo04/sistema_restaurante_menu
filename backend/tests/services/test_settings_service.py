from app.models.app_settings import AppSettings, MenuLayout
from app.schemas import SettingsUpdate
from sqlmodel import select


def test_get_returns_grid_by_default_when_unset(settings_service):
    assert settings_service.get() == MenuLayout.GRID


def test_update_persists_and_get_returns_it(settings_service):
    setting = SettingsUpdate(layout=MenuLayout.LIST)

    result = settings_service.update(setting.layout)

    assert result == MenuLayout.LIST
    assert settings_service.get() == MenuLayout.LIST


def test_update_overwrites_previous_value(settings_service):
    settings_service.update(MenuLayout.CAROUSEL)

    settings_service.update(MenuLayout.GRID)

    assert settings_service.get() == MenuLayout.GRID


def test_update_keeps_single_singleton_row(settings_service, db_session):
    settings_service.update(MenuLayout.LIST)
    settings_service.update(MenuLayout.CAROUSEL)
    settings_service.update(MenuLayout.GRID)

    rows = db_session.exec(select(AppSettings)).all()

    assert len(rows) == 1
    assert rows[0].id == 1
