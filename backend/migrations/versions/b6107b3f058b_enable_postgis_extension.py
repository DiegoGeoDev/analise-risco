"""enable postgis extension

Revision ID: b6107b3f058b
Revises: 
Create Date: 2026-07-11 11:32:24.404545

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b6107b3f058b'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Habilita a extensão PostGIS (tipos e funções geoespaciais)."""
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")


def downgrade() -> None:
    """Remove a extensão PostGIS (só roda quando nenhuma tabela usa geometry)."""
    op.execute("DROP EXTENSION IF EXISTS postgis")
