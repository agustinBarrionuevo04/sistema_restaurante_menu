import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db import get_session
from app.models.category import Category
from app.models.product import Product
from app.schemas import CategoryCreate, CategoryUpdate, CategoryOut

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[CategoryOut])
def list_categories(session: Session = Depends(get_session)):
    categories = session.exec(select(Category).order_by(Category.order)).all()
    return categories


@router.post("", response_model=CategoryOut, status_code=201)
def create_category(data: CategoryCreate, session: Session = Depends(get_session)):
    category = Category(name=data.name, order=data.order)
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@router.patch("/{id}", response_model=CategoryOut)
def update_category(id: uuid.UUID, data: CategoryUpdate, session: Session = Depends(get_session)):
    category = session.get(Category, id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(category, key, value)
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@router.delete("/{id}", status_code=204)
def delete_category(id: uuid.UUID, session: Session = Depends(get_session)):
    category = session.get(Category, id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    product_count = session.exec(
        select(Product).where(Product.category_id == id)
    ).first()
    if product_count:
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar la categoría porque tiene productos asociados",
        )

    session.delete(category)
    session.commit()
