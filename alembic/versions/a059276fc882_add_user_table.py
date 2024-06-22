"""Add user table

Revision ID: a059276fc882
Revises: aeac2ae3e225
Create Date: 2024-06-22 22:10:44.846010

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a059276fc882'
down_revision: Union[str, None] = 'aeac2ae3e225'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("username", sa.String(), nullable=False, unique=True),
        sa.Column("password", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("approved", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("admin", sa.Boolean(), nullable=False, server_default=sa.text("false"))
    )


def downgrade() -> None:
    op.drop_table("users")
