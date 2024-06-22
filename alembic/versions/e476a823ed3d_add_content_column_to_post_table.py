"""Add content column to post table

Revision ID: e476a823ed3d
Revises: aeac2ae3e225
Create Date: 2024-06-22 21:28:58.749095

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e476a823ed3d'
down_revision: Union[str, None] = 'aeac2ae3e225'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('products', sa.Column('is_available', sa.Boolean(), nullable=False))


def downgrade() -> None:
    pass
