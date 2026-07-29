import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db import get_session
from app.models.addon import AddOn
from app.models.product_addon import ProductAddOn
from app.schemas import AddOnCreate, AddOnUpdate, AddOnOut

router = APIRouter(prefix="/addons", tags=["addons"])


@router.get("", response_model=list[AddOnOut])
def list_addons(session: Session = Depends(get_session)):
    addons = session.exec(select(AddOn)).all()
    return addons


@router.post("", response_model=AddOnOut, status_code=201)
def create_addon(data: AddOnCreate, session: Session = Depends(get_session)):
    addon = AddOn(name=data.name, default_price=data.default_price)
    session.add(addon)
    session.commit()
    session.refresh(addon)
    return addon


@router.patch("/{id}", response_model=AddOnOut)
def update_addon(id: uuid.UUID, data: AddOnUpdate, session: Session = Depends(get_session)):
    addon = session.get(AddOn, id)
    if not addon:
        raise HTTPException(status_code=404, detail="Adicional no encontrado")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(addon, key, value)

    session.add(addon)
    session.commit()
    session.refresh(addon)
    return addon


@router.delete("/{id}", status_code=204)
def delete_addon(id: uuid.UUID, session: Session = Depends(get_session)):
    addon = session.get(AddOn, id)
    if not addon:
        raise HTTPException(status_code=404, detail="Adicional no encontrado")

    in_use = session.exec(
        select(ProductAddOn).where(ProductAddOn.addon_id == id)
    ).first()
    if in_use:
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar el adicional porque está en uso en productos",
        )

    session.delete(addon)
    session.commit()
