"""merge

Revision ID: c30e1718a3c9
Revises: 1b51da2727d2, d814e6b5d46c
Create Date: 2026-04-28 21:42:58.738291

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'c30e1718a3c9'
down_revision: Union[str, Sequence[str], None] = ('1b51da2727d2', 'd814e6b5d46c')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
