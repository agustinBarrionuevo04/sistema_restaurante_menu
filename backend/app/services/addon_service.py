from dataclasses import dataclass
from uuid import UUID

from fastapi import HTTPException
from sqlmodel import select

from app.models.addon import AddOn
from app.models.product_addon import ProductAddOn
from app.schemas import AddOnCreate, AddOnUpdate
from app.services.base import BaseService


@dataclass
class AddOnService(BaseService):
    """Servicio de negocio para el CRUD de adicionales."""

    def list(self) -> list[AddOn]:
        """Lista todos los adicionales."""
        return list(self.session.exec(select(AddOn)).all())

    def create(self, data: AddOnCreate) -> AddOn:
        """Crea un nuevo adicional."""
        return self.commit_refresh(
            AddOn(name=data.name, default_price=data.default_price)
        )

    def update(self, id: UUID, data: AddOnUpdate) -> AddOn:
        """Actualiza solo los campos enviados de un adicional existente."""
        addon = self.get_or_404(AddOn, id, "Adicional no encontrado")
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(addon, key, value)
        return self.commit_refresh(addon)

    def delete(self, id: UUID) -> None:
        """Elimina un adicional; rechaza si está en uso por algún producto."""
        addon = self.get_or_404(AddOn, id, "Adicional no encontrado")
        if self.session.exec(
            select(ProductAddOn).where(ProductAddOn.addon_id == id)
        ).first():
            raise HTTPException(
                status_code=409,
                detail="No se puede eliminar el adicional porque está en uso en productos",
            )
        self.session.delete(addon)
        self.session.commit()
