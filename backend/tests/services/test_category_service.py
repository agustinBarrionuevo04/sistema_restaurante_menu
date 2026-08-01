import uuid

import pytest
from app.models.category import Category
from app.models.product import Product, ProductStatus
from app.schemas import CategoryCreate, CategoryUpdate
from app.services import CategoryService
from fastapi import HTTPException
from sqlmodel import select


@pytest.fixture()
def category_service(db_session):
    return CategoryService(session=db_session)


def _create_category(category_service, name="Entradas", order=1) -> Category:
    return category_service.create(CategoryCreate(name=name, order=order))


def test_create_category(category_service):
    cat = _create_category(category_service, name="Postres", order=2)

    assert cat.name == "Postres"
    assert cat.order == 2
    assert cat.id is not None


def test_list_returns_ordered_categories(category_service):
    _create_category(category_service, name="B", order=2)
    _create_category(category_service, name="A", order=1)

    cats = category_service.list()

    assert [c.name for c in cats] == ["A", "B"]


def test_update_only_changes_sent_fields(category_service):
    cat = _create_category(category_service, name="Entradas", order=1)

    updated = category_service.update(cat.id, CategoryUpdate(name="Entradas y más"))

    assert updated.name == "Entradas y más"
    assert updated.order == 1


def test_update_raises_404_for_missing(category_service):
    with pytest.raises(HTTPException) as exc_info:
        category_service.update(uuid.uuid4(), CategoryUpdate(name="X"))
    assert exc_info.value.status_code == 404


def test_delete_category(category_service, db_session):
    cat = _create_category(category_service)

    category_service.delete(cat.id)

    assert db_session.exec(select(Category)).all() == []


def test_delete_raises_409_when_category_has_products(category_service, db_session):
    cat = _create_category(category_service)
    db_session.add(
        Product(
            category_id=cat.id,
            name="Bife",
            description="",
            base_price=18.0,
            status=ProductStatus.ACTIVE,
        )
    )
    db_session.commit()

    with pytest.raises(HTTPException) as exc_info:
        category_service.delete(cat.id)
    assert exc_info.value.status_code == 409


def test_delete_raises_404_for_missing(category_service):
    with pytest.raises(HTTPException) as exc_info:
        category_service.delete(uuid.uuid4())
    assert exc_info.value.status_code == 404
