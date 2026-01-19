"""Add indexes for created_at columns

Revision ID: bb6db7cd097d
Revises: 030671424d3e
Create Date: 2026-01-19 14:46:55.827132

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb6db7cd097d'
down_revision: Union[str, Sequence[str], None] = '030671424d3e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_index('ix_images_created_at', 'images', ['created_at'])
    op.create_index('ix_users_created_at', 'users', ['created_at'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('ix_images_created_at', table_name='images')
    op.drop_index('ix_users_created_at', table_name='users')
