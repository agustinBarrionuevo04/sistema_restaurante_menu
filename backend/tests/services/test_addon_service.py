import uuid

import pytest
from app.models.addon import AddOn
from app.models.product import Product, ProductStatus
from app.models.product_addon import ProductAddOn
from app.schemas import AddOnCreate, AddOnUpdate
from app.services import AddOnService
from fastapi import HTTPException
from sqlmodel import select


@pytest.fixture()
def addon_service(db_session):
    return AddOnService(session=db_session)


def _create_addon(addon_service, name="Queso extra", price=1.50) -> AddOn:
    return addon_service.create(AddOnCreate(name=name, default_price=price))


def test_create_addon(addon_service):
    addon = _create_addon(addon_service)

    assert addon.name == "Queso extra"
    assert float(addon.default_price) == 1.50


def test_list_addons(addon_service):
    _create_addon(addon_service, name="A", price=1.0)
    _create_addon(addon_service, name="B", price=2.0)

    addons = addon_service.list()

    assert len(addons) == 2
    assert {a.name for a in addons} == {"A", "B"}


def test_update_addon(addon_service):
    addon = _create_addon(addon_service)

    updated = addon_service.update(addon.id, AddOnUpdate(default_price=2.50))

    assert float(updated.default_price) == 2.50
    assert updated.name == "Queso extra"


def test_update_addon_404(addon_service):
    with pytest.raises(HTTPException) as exc_info:
        addon_service.update(uuid.uuid4(), AddOnUpdate(name="X"))
    assert exc_info.value.status_code == 404


def test_delete_addon(addon_service, db_session):
    addon = _create_addon(addon_service)

    addon_service.delete(addon.id)

    assert db_session.exec(select(AddOn)).all() == []


def test_delete_addon_404(addon_service):
    with pytest.raises(HTTPException) as exc_info:
        addon_service.delete(uuid.uuid4())
    assert exc_info.value.status_code == 404


def test_delete_addon_409_when_in_use(addon_service, db_session, a_category):
    addon = _create_addon(addon_service)
    product = Product(
        category_id=a_category.id,
        name="Ojo de bife",
        description="",
        base_price=22.0,
        status=ProductStatus.ACTIVE,
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)
    db_session.add(ProductAddOn(product_id=product.id, addon_id=addon.id))
    db_session.commit()

    with pytest.raises(HTTPException) as exc_info:
        addon_service.delete(addon.id)
    assert exc_info.value.status_code == 409
