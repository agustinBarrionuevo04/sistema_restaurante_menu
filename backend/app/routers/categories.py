import uuid

from fastapi import APIRouter, Depends

from app.deps import get_category_service
from app.schemas import CategoryCreate, CategoryOut, CategoryUpdate
from app.services import CategoryService

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[CategoryOut])
def list_categories(service: CategoryService = Depends(get_category_service)):
    """Lista las categorías ordenadas."""
    return service.list()


@router.post("", response_model=CategoryOut, status_code=201)
def create_category(
    data: CategoryCreate, service: CategoryService = Depends(get_category_service)
):
    """Crea una nueva categoría."""
    return service.create(data)


@router.patch("/{id}", response_model=CategoryOut)
def update_category(
    id: uuid.UUID,
    data: CategoryUpdate,
    service: CategoryService = Depends(get_category_service),
):
    """Actualiza una categoría existente."""
    return service.update(id, data)


@router.delete("/{id}", status_code=204)
def delete_category(
    id: uuid.UUID, service: CategoryService = Depends(get_category_service)
):
    """Elimina una categoría (rechaza si tiene productos)."""
    service.delete(id)
