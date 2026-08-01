import uuid

from fastapi import APIRouter, Depends

from app.deps import get_addon_service
from app.schemas import AddOnCreate, AddOnOut, AddOnUpdate
from app.services import AddOnService

router = APIRouter(prefix="/addons", tags=["addons"])


@router.get("", response_model=list[AddOnOut])
def list_addons(service: AddOnService = Depends(get_addon_service)):
    """Lista los adicionales."""
    return service.list()


@router.post("", response_model=AddOnOut, status_code=201)
def create_addon(data: AddOnCreate, service: AddOnService = Depends(get_addon_service)):
    """Crea un nuevo adicional."""
    return service.create(data)


@router.patch("/{id}", response_model=AddOnOut)
def update_addon(
    id: uuid.UUID,
    data: AddOnUpdate,
    service: AddOnService = Depends(get_addon_service),
):
    """Actualiza un adicional existente."""
    return service.update(id, data)


@router.delete("/{id}", status_code=204)
def delete_addon(id: uuid.UUID, service: AddOnService = Depends(get_addon_service)):
    """Elimina un adicional (rechaza si está en uso)."""
    service.delete(id)
