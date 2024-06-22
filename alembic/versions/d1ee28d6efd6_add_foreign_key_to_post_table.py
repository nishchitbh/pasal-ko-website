"""Add foreign-key to product table

Revision ID: d1ee28d6efd6
Revises: a059276fc882
Create Date: 2024-06-22 22:18:36.377783

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d1ee28d6efd6"
down_revision: Union[str, None] = "a059276fc882"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("products", sa.Column("owner_id", sa.Integer, nullable=False))
    op.create_foreign_key(
        "products_users_fk",
        source_table="products",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE"
    )


def downgrade() -> None:
    op.drop_constraint('products_users_fk', table_name='products')
