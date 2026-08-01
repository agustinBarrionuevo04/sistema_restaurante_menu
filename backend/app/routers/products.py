import uuid

from fastapi import APIRouter, Depends, Query

from app.deps import get_product_service
from app.models.product import ProductStatus
from app.schemas import (
    ProductAddOnCreate,
    ProductAddOnOut,
    ProductCreate,
    ProductOut,
    ProductUpdate,
)
from app.services import ProductService

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductOut])
def list_products(
    category_id: uuid.UUID | None = Query(None),
    status: ProductStatus | None = Query(None),
    service: ProductService = Depends(get_product_service),
):
    """Lista productos según filtros opcionales."""
    products = service.list(category_id=category_id, status=status)
    return [service.to_out(p) for p in products]


@router.get("/{id}", response_model=ProductOut)
def get_product(id: uuid.UUID, service: ProductService = Depends(get_product_service)):
    """Obtiene un producto por id con sus adicionales."""
    return service.to_out(service.get(id))


@router.post("", response_model=ProductOut, status_code=201)
def create_product(
    data: ProductCreate, service: ProductService = Depends(get_product_service)
):
    """Crea un nuevo producto."""
    return service.to_out(service.create(data))


@router.patch("/{id}", response_model=ProductOut)
def update_product(
    id: uuid.UUID,
    data: ProductUpdate,
    service: ProductService = Depends(get_product_service),
):
    """Actualiza parcialmente un producto."""
    return service.to_out(service.update(id, data))


@router.delete("/{id}", status_code=204)
def delete_product(
    id: uuid.UUID, service: ProductService = Depends(get_product_service)
):
    """Elimina un producto de forma definitiva."""
    service.delete(id)


@router.post("/{id}/addons", response_model=ProductAddOnOut, status_code=201)
def associate_addon(
    id: uuid.UUID,
    data: ProductAddOnCreate,
    service: ProductService = Depends(get_product_service),
):
    """Asocia un adicional a un producto."""
    return service.associate_addon(id, data)


@router.delete("/{id}/addons/{addon_id}", status_code=204)
def disassociate_addon(
    id: uuid.UUID,
    addon_id: uuid.UUID,
    service: ProductService = Depends(get_product_service),
):
    """Desasocia un adicional de un producto."""
    service.disassociate_addon(id, addon_id)
