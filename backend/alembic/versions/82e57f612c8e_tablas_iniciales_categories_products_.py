"""tablas iniciales (categories, products, addons, product_addons, app_settings)

Revision ID: 82e57f612c8e
Revises:
Create Date: 2026-07-31 21:13:29.172105

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '82e57f612c8e'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Crea el esquema inicial del sistema de carta digital."""
    op.create_table(
        'categories',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('name', sa.VARCHAR(length=255), nullable=False),
        sa.Column('order', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'addons',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('name', sa.VARCHAR(length=255), nullable=False),
        sa.Column('default_price', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'app_settings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('layout', sa.Enum('list', 'grid', 'carousel', name='menulayout'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'products',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('category_id', sa.Uuid(), nullable=False),
        sa.Column('name', sa.VARCHAR(length=255), nullable=False),
        sa.Column('description', sa.VARCHAR(), nullable=False),
        sa.Column('base_price', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('image_url', sa.VARCHAR(), nullable=True),
        sa.Column(
            'status',
            sa.Enum('active', 'suspended', name='productstatus'),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'product_addons',
        sa.Column('product_id', sa.Uuid(), nullable=False),
        sa.Column('addon_id', sa.Uuid(), nullable=False),
        sa.Column('price_override', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.ForeignKeyConstraint(['addon_id'], ['addons.id']),
        sa.ForeignKeyConstraint(['product_id'], ['products.id']),
        sa.PrimaryKeyConstraint('product_id', 'addon_id'),
    )


def downgrade() -> None:
    """Elimina el esquema inicial en orden inverso."""
    op.drop_table('product_addons')
    op.drop_table('products')
    op.drop_table('app_settings')
    op.drop_table('addons')
    op.drop_table('categories')
