from dataclasses import dataclass
from uuid import UUID

from fastapi import HTTPException
from sqlmodel import select

from app.models.category import Category
from app.models.product import Product
from app.schemas import CategoryCreate, CategoryUpdate
from app.services.base import BaseService


@dataclass
class CategoryService(BaseService):
    """Servicio de negocio para el CRUD de categorías."""

    def list(self) -> list[Category]:
        """Lista las categorías ordenadas por su campo :attr:`order`."""
        return list(self.session.exec(select(Category).order_by(Category.order)).all())

    def create(self, data: CategoryCreate) -> Category:
        """Crea una nueva categoría."""
        return self.commit_refresh(Category(name=data.name, order=data.order))

    def update(self, id: UUID, data: CategoryUpdate) -> Category:
        """Actualiza solo los campos enviados de una categoría existente."""
        category = self.get_or_404(Category, id, "Categoría no encontrada")
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(category, key, value)
        return self.commit_refresh(category)

    def delete(self, id: UUID) -> None:
        """Elimina una categoría; rechaza si tiene productos asociados."""
        category = self.get_or_404(Category, id, "Categoría no encontrada")
        if self.session.exec(select(Product).where(Product.category_id == id)).first():
            raise HTTPException(
                status_code=409,
                detail="No se puede eliminar la categoría porque tiene productos asociados",
            )
        self.session.delete(category)
        self.session.commit()
