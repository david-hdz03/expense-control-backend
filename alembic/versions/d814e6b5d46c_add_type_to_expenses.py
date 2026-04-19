"""add type to expenses

Revision ID: d814e6b5d46c
Revises: 326bdcfe4e14
Create Date: 2026-04-12 20:17:30.264891

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd814e6b5d46c'
down_revision: Union[str, Sequence[str], None] = '326bdcfe4e14'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "expenses",
        sa.Column(
            "type",
            sa.String(length=20),
            nullable=False,
            server_default="expense",
        ),
    )
    op.create_index(
        "ix_expenses_type", "expenses", ["type"], unique=False
    )


def downgrade() -> None:
    op.drop_index("ix_expenses_type", table_name="expenses")
    op.drop_column("expenses", "type")
