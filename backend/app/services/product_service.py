from dataclasses import dataclass
from uuid import UUID

from fastapi import HTTPException
from sqlmodel import select

from app.models.addon import AddOn
from app.models.product import Product, ProductStatus
from app.models.product_addon import ProductAddOn
from app.schemas import (
    AddOnOut,
    ProductAddOnCreate,
    ProductAddOnOut,
    ProductCreate,
    ProductOut,
    ProductUpdate,
)
from app.services.base import BaseService


@dataclass
class ProductService(BaseService):
    """Servicio de negocio para productos y sus adicionales."""

    def to_out(self, product: Product) -> ProductOut:
        """Proyecta un producto a ProductOut, cargando sus adicionales asociados."""
        product_addons = self.session.exec(
            select(ProductAddOn).where(ProductAddOn.product_id == product.id)
        ).all()

        addons_out: list[ProductAddOnOut] = []
        for pa in product_addons:
            addon = self.session.get(AddOn, pa.addon_id)
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

    def list(
        self,
        category_id: UUID | None = None,
        status: ProductStatus | None = None,
    ) -> list[Product]:
        """Lista productos aplicando filtros opcionales por categoría y estado."""
        query = select(Product)
        if category_id is not None:
            query = query.where(Product.category_id == category_id)
        if status is not None:
            query = query.where(Product.status == status)
        return list(self.session.exec(query).all())

    def get(self, id: UUID) -> Product:
        """Devuelve un producto por id."""
        return self.get_or_404(Product, id, "Producto no encontrado")

    def create(self, data: ProductCreate) -> Product:
        """Crea un nuevo producto."""
        product = Product(
            category_id=data.category_id,
            name=data.name,
            description=data.description,
            base_price=data.base_price,
            image_url=data.image_url,
            status=data.status,
        )
        return self.commit_refresh(product)

    def update(self, id: UUID, data: ProductUpdate) -> Product:
        """Actualiza solo los campos enviados de un producto existente."""
        product = self.get_or_404(Product, id, "Producto no encontrado")
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(product, key, value)
        return self.commit_refresh(product)

    def delete(self, id: UUID) -> None:
        """Elimina un producto de forma definitiva."""
        product = self.get_or_404(Product, id, "Producto no encontrado")
        self.session.delete(product)
        self.session.commit()

    def associate_addon(
        self, product_id: UUID, data: ProductAddOnCreate
    ) -> ProductAddOnOut:
        """Asocia un adicional ya existente a un producto."""
        self.get_or_404(Product, product_id, "Producto no encontrado")
        addon = self.get_or_404(AddOn, data.addon_id, "Adicional no encontrado")

        existing = self.session.get(ProductAddOn, (product_id, data.addon_id))
        if existing:
            raise HTTPException(
                status_code=409,
                detail="El adicional ya está asociado a este producto",
            )

        pa = ProductAddOn(
            product_id=product_id,
            addon_id=data.addon_id,
            price_override=data.price_override,
        )
        self.commit_refresh(pa)

        return ProductAddOnOut(
            addon=AddOnOut.model_validate(addon),
            price_override=pa.price_override,
        )

    def disassociate_addon(self, product_id: UUID, addon_id: UUID) -> None:
        """Desasocia un adicional de un producto."""
        self.get_or_404(Product, product_id, "Producto no encontrado")
        pa = self.session.get(ProductAddOn, (product_id, addon_id))
        if pa is None:
            raise HTTPException(status_code=404, detail="Asociación no encontrada")
        self.session.delete(pa)
        self.session.commit()
