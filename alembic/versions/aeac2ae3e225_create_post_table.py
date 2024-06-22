"""Create post table

Revision ID: aeac2ae3e225
Revises: 
Create Date: 2024-06-22 21:14:24.160496

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aeac2ae3e225'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('products', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('name', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_table('products')
