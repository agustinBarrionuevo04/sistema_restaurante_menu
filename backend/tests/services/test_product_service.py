import uuid

import pytest
from app.models.product import Product, ProductStatus
from app.models.product_addon import ProductAddOn
from app.schemas import (
    ProductAddOnCreate,
    ProductCreate,
    ProductUpdate,
)
from app.services import ProductService
from fastapi import HTTPException


@pytest.fixture()
def product_service(db_session):
    return ProductService(session=db_session)


def _create_product(
    product_service,
    a_category,
    name="Bife de chorizo",
    price=18.0,
    status=ProductStatus.ACTIVE,
    description="Bife 300g",
) -> Product:
    data = ProductCreate(
        category_id=a_category.id,
        name=name,
        base_price=price,
        description=description,
        status=status,
    )
    return product_service.create(data)


def test_create_product(product_service, a_category):
    p = _create_product(product_service, a_category)

    assert p.name == "Bife de chorizo"
    assert p.category_id == a_category.id
    assert float(p.base_price) == 18.0
    assert p.status == ProductStatus.ACTIVE


def test_get_product(product_service, a_category):
    p = _create_product(product_service, a_category)

    found = product_service.get(p.id)

    assert found.id == p.id
    assert found.name == p.name


def test_get_product_404(product_service):
    with pytest.raises(HTTPException) as exc_info:
        product_service.get(uuid.uuid4())
    assert exc_info.value.status_code == 404


def test_list_products(product_service, a_category):
    _create_product(product_service, a_category, name="A")
    _create_product(product_service, a_category, name="B")

    result = product_service.list()

    assert len(result) == 2


def test_list_filters_by_category(product_service, db_session, a_category):
    from app.models.category import Category

    other = Category(name="Bebidas", order=2)
    db_session.add(other)
    db_session.commit()
    db_session.refresh(other)

    _create_product(product_service, a_category, name="En parrilla")
    _create_product(product_service, other, name="Vino")

    result = product_service.list(category_id=a_category.id)

    assert {r.name for r in result} == {"En parrilla"}


def test_list_filters_by_status(product_service, a_category):
    _create_product(
        product_service, a_category, name="Activo", status=ProductStatus.ACTIVE
    )
    _create_product(
        product_service, a_category, name="Pausado", status=ProductStatus.SUSPENDED
    )

    result = product_service.list(status=ProductStatus.SUSPENDED)

    assert [r.name for r in result] == ["Pausado"]


def test_update_only_sent_fields(product_service, a_category):
    p = _create_product(product_service, a_category, name="Original", price=18.0)

    updated = product_service.update(p.id, ProductUpdate(name="Renombrado"))

    assert updated.name == "Renombrado"
    assert float(updated.base_price) == 18.0


def test_update_404(product_service):
    with pytest.raises(HTTPException) as exc_info:
        product_service.update(uuid.uuid4(), ProductUpdate(name="X"))
    assert exc_info.value.status_code == 404


def test_delete_product(product_service, a_category, db_session):
    from sqlmodel import select

    p = _create_product(product_service, a_category)

    product_service.delete(p.id)

    assert db_session.exec(select(Product)).all() == []


def test_delete_404(product_service):
    with pytest.raises(HTTPException) as exc_info:
        product_service.delete(uuid.uuid4())
    assert exc_info.value.status_code == 404


def test_to_out_includes_addons(product_service, a_category, an_addon):
    p = _create_product(product_service, a_category)
    product_service.associate_addon(
        p.id, ProductAddOnCreate(addon_id=an_addon.id, price_override=2.0)
    )

    out = product_service.to_out(p)

    assert len(out.addons) == 1
    assert out.addons[0].addon.name == an_addon.name
    assert float(out.addons[0].price_override) == 2.0


def test_associate_addon(product_service, a_category, an_addon):
    p = _create_product(product_service, a_category)

    result = product_service.associate_addon(
        p.id, ProductAddOnCreate(addon_id=an_addon.id)
    )

    assert result.addon.id == an_addon.id
    assert result.price_override is None


def test_associate_addon_duplicate_raises_409(product_service, a_category, an_addon):
    p = _create_product(product_service, a_category)
    product_service.associate_addon(p.id, ProductAddOnCreate(addon_id=an_addon.id))

    with pytest.raises(HTTPException) as exc_info:
        product_service.associate_addon(p.id, ProductAddOnCreate(addon_id=an_addon.id))
    assert exc_info.value.status_code == 409


def test_associate_addon_on_missing_product_404(product_service, an_addon):
    with pytest.raises(HTTPException) as exc_info:
        product_service.associate_addon(
            uuid.uuid4(), ProductAddOnCreate(addon_id=an_addon.id)
        )
    assert exc_info.value.status_code == 404


def test_disassociate_addon(product_service, a_category, an_addon, db_session):
    from sqlmodel import select

    p = _create_product(product_service, a_category)
    product_service.associate_addon(p.id, ProductAddOnCreate(addon_id=an_addon.id))

    product_service.disassociate_addon(p.id, an_addon.id)

    assert db_session.exec(select(ProductAddOn)).all() == []


def test_disassociate_addon_404(product_service, a_category):
    p = _create_product(product_service, a_category)

    with pytest.raises(HTTPException) as exc_info:
        product_service.disassociate_addon(p.id, uuid.uuid4())
    assert exc_info.value.status_code == 404
