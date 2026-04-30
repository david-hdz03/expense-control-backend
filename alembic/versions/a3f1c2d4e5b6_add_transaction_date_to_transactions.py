"""add transaction_date to transactions

Revision ID: a3f1c2d4e5b6
Revises: 8fe4c7003f78
Create Date: 2026-04-29 00:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = 'a3f1c2d4e5b6'
down_revision: Union[str, Sequence[str], None] = '8fe4c7003f78'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'transactions',
        sa.Column(
            'transaction_date',
            sa.DateTime(),
            nullable=False,
            server_default=sa.text('CURRENT_TIMESTAMP'),
        ),
    )
    op.create_index(
        'ix_transactions_transaction_date',
        'transactions',
        ['transaction_date'],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index('ix_transactions_transaction_date', table_name='transactions')
    op.drop_column('transactions', 'transaction_date')
