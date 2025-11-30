"""create admin user

Revision ID: 002
Revises: 001
Create Date: 2024-03-30 13:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create default admin user
    # Password is 'admin'
    op.execute(
        "INSERT INTO users (email, password_hash, created_at, updated_at) "
        "VALUES ('admin@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxwKc.60rScphF.1k1.Zz1q.k1.i', NOW(), NOW()) "
        "ON CONFLICT (email) DO NOTHING"
    )


def downgrade() -> None:
    op.execute("DELETE FROM users WHERE email = 'admin@example.com'")

