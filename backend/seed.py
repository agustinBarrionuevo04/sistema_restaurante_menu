import os
from decimal import Decimal

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

from app.models.category import Category
from app.models.addon import AddOn
from app.models.product import Product, ProductStatus
from app.models.product_addon import ProductAddOn

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./menu.db")
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})


def seed():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        categories = [
            Category(name="Entradas", order=1),
            Category(name="Parrilla", order=2),
            Category(name="Guarniciones", order=3),
            Category(name="Bebidas", order=4),
            Category(name="Postres", order=5),
        ]
        session.add_all(categories)
        session.flush()

        addons = [
            AddOn(name="Queso extra", default_price=Decimal("1.50")),
            AddOn(name="Cheddar", default_price=Decimal("2.00")),
            AddOn(name="Panceta", default_price=Decimal("2.50")),
            AddOn(name="Huevo frito", default_price=Decimal("1.00")),
            AddOn(name="Porción de papas", default_price=Decimal("3.00")),
            AddOn(name="Salsa barbacoa", default_price=Decimal("0.80")),
            AddOn(name="Crema de leche", default_price=Decimal("0.60")),
        ]
        session.add_all(addons)
        session.flush()

        cat = {c.name: c for c in categories}
        ad = {a.name: a for a in addons}

        def add_product(
            category: Category,
            name: str,
            description: str,
            price: Decimal,
            product_addons: list[AddOn] = None,
        ):
            p = Product(
                category_id=category.id,
                name=name,
                description=description,
                base_price=price,
                image_url=f"https://placehold.co/400x300/EEE/333?text={name.replace(' ', '+')}",
                status=ProductStatus.ACTIVE,
            )
            session.add(p)
            session.flush()

            if product_addons:
                for a in product_addons:
                    session.add(ProductAddOn(product_id=p.id, addon_id=a.id))

        add_product(
            cat["Entradas"],
            "Provoleta",
            "Provolone a la parrilla con orégano y tomates cherrys",
            Decimal("8.50"),
        )

        add_product(
            cat["Entradas"],
            "Mollejas",
            "Mollejas de corazón a la parrilla con limón",
            Decimal("10.00"),
        )

        add_product(
            cat["Entradas"],
            "Chorizo criollo",
            "Chorizo parrillero con chimichurri",
            Decimal("6.00"),
        )

        add_product(
            cat["Entradas"],
            "Empanadas de carne (x3)",
            "Empanadas caseras de carne cortada a cuchillo",
            Decimal("7.50"),
        )

        add_product(
            cat["Parrilla"],
            "Bife de chorizo",
            "Bife de chorizo 300g con guarnición a elección",
            Decimal("18.00"),
            [ad["Porción de papas"]],
        )

        add_product(
            cat["Parrilla"],
            "Ojo de bife",
            "Ojo de bife 280g, jugoso y tierno",
            Decimal("22.00"),
            [ad["Porción de papas"], ad["Crema de leche"]],
        )

        add_product(
            cat["Parrilla"],
            "Asado de tira",
            "Tira de asado 400g bien jugosa",
            Decimal("16.00"),
            [ad["Porción de papas"]],
        )

        add_product(
            cat["Parrilla"],
            "Hamburguesa completa",
            "Hamburguesa artesanal 200g con lechuga, tomate y cebolla caramelizada",
            Decimal("12.00"),
            [ad["Queso extra"], ad["Cheddar"], ad["Panceta"], ad["Huevo frito"], ad["Porción de papas"]],
        )

        add_product(
            cat["Parrilla"],
            "Pechuga de pollo",
            "Pechuga de pollo a la parrilla con ensalada",
            Decimal("14.00"),
            [ad["Porción de papas"]],
        )

        add_product(
            cat["Guarniciones"],
            "Papas fritas",
            "Papas fritas crocantes con sal gruesa",
            Decimal("4.50"),
            [ad["Crema de leche"], ad["Salsa barbacoa"]],
        )

        add_product(
            cat["Guarniciones"],
            "Ensalada mixta",
            "Lechuga, tomate, zanahoria y cebolla",
            Decimal("5.00"),
        )

        add_product(
            cat["Guarniciones"],
            "Puré de papas",
            "Puré de papas cremoso con manteca",
            Decimal("5.50"),
        )

        add_product(
            cat["Bebidas"],
            "Coca-Cola (lata)",
            "",
            Decimal("2.50"),
        )

        add_product(
            cat["Bebidas"],
            "Cerveza artesanal Rubia",
            "Cerveza rubia tirada 500cc",
            Decimal("6.00"),
        )

        add_product(
            cat["Bebidas"],
            "Agua mineral 500ml",
            "",
            Decimal("2.00"),
        )

        add_product(
            cat["Bebidas"],
            "Vino Malbec",
            "Copa de vino Malbec 250cc",
            Decimal("7.00"),
        )

        add_product(
            cat["Postres"],
            "Flan con dulce de leche",
            "Flan casero con dulce de leche y crema",
            Decimal("6.00"),
        )

        add_product(
            cat["Postres"],
            "Helado (2 bochas)",
            "Helado artesanal, dos bochas a elección",
            Decimal("7.00"),
        )

        add_product(
            cat["Postres"],
            "Chocotorta",
            "Porción de chocotorta tradicional",
            Decimal("6.50"),
        )

        session.commit()

    print("Seed completado exitosamente")


if __name__ == "__main__":
    seed()
