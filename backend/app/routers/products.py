import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.db import get_session
from app.models.product import Product, ProductStatus
from app.models.product_addon import ProductAddOn
from app.models.addon import AddOn
from app.schemas import (
    ProductCreate,
    ProductUpdate,
    ProductOut,
    ProductAddOnOut,
    ProductAddOnCreate,
    AddOnOut,
)

router = APIRouter(prefix="/products", tags=["products"])


def product_to_out(product: Product, session: Session) -> ProductOut:
    product_addons = session.exec(
        select(ProductAddOn).where(ProductAddOn.product_id == product.id)
    ).all()

    addons_out = []
    for pa in product_addons:
        addon = session.get(AddOn, pa.addon_id)
        addons_out.append(
            ProductAddOnOut(
                addon=AddOnOut.model_validate(addon),
                price_override=pa.price_override,
            )
        )

    return ProductOut(
        id=product.id,
        category_id=product.category_id,
        name=product.name,
        description=product.description,
        base_price=product.base_price,
        image_url=product.image_url,
        status=product.status,
        addons=addons_out,
    )


@router.get("", response_model=list[ProductOut])
def list_products(
    category_id: Optional[uuid.UUID] = Query(None),
    status: Optional[ProductStatus] = Query(None),
    session: Session = Depends(get_session),
):
    query = select(Product)
    if category_id:
        query = query.where(Product.category_id == category_id)
    if status:
        query = query.where(Product.status == status)

    products = session.exec(query).all()
    return [product_to_out(p, session) for p in products]


@router.get("/{id}", response_model=ProductOut)
def get_product(id: uuid.UUID, session: Session = Depends(get_session)):
    product = session.get(Product, id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product_to_out(product, session)


@router.post("", response_model=ProductOut, status_code=201)
def create_product(data: ProductCreate, session: Session = Depends(get_session)):
    product = Product(
        category_id=data.category_id,
        name=data.name,
        description=data.description,
        base_price=data.base_price,
        image_url=data.image_url,
        status=data.status,
    )
    session.add(product)
    session.commit()
    session.refresh(product)
    return product_to_out(product, session)


@router.patch("/{id}", response_model=ProductOut)
def update_product(id: uuid.UUID, data: ProductUpdate, session: Session = Depends(get_session)):
    product = session.get(Product, id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)

    session.add(product)
    session.commit()
    session.refresh(product)
    return product_to_out(product, session)


@router.delete("/{id}", status_code=204)
def delete_product(id: uuid.UUID, session: Session = Depends(get_session)):
    product = session.get(Product, id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    session.delete(product)
    session.commit()


@router.post("/{id}/addons", response_model=ProductAddOnOut, status_code=201)
def associate_addon(
    id: uuid.UUID, data: ProductAddOnCreate, session: Session = Depends(get_session)
):
    product = session.get(Product, id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    addon = session.get(AddOn, data.addon_id)
    if not addon:
        raise HTTPException(status_code=404, detail="Adicional no encontrado")

    existing = session.get(ProductAddOn, (id, data.addon_id))
    if existing:
        raise HTTPException(status_code=409, detail="El adicional ya está asociado a este producto")

    pa = ProductAddOn(
        product_id=id,
        addon_id=data.addon_id,
        price_override=data.price_override,
    )
    session.add(pa)
    session.commit()
    session.refresh(pa)

    return ProductAddOnOut(
        addon=AddOnOut.model_validate(addon),
        price_override=pa.price_override,
    )


@router.delete("/{id}/addons/{addon_id}", status_code=204)
def disassociate_addon(
    id: uuid.UUID, addon_id: uuid.UUID, session: Session = Depends(get_session)
):
    pa = session.get(ProductAddOn, (id, addon_id))
    if not pa:
        raise HTTPException(status_code=404, detail="Asociación no encontrada")
    session.delete(pa)
    session.commit()
