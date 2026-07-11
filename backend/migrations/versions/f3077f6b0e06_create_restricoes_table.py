"""create restricoes table

Revision ID: f3077f6b0e06
Revises: b6107b3f058b
Create Date: 2026-07-11 13:57:39.230797

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from geoalchemy2 import Geometry


# revision identifiers, used by Alembic.
revision: str = 'f3077f6b0e06'
down_revision: Union[str, Sequence[str], None] = 'b6107b3f058b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Cria a tabela genérica de restrições ambientais."""
    op.create_table(
        "restricoes",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("tipo", sa.String(length=50), nullable=False),
        sa.Column("fonte", sa.String(length=50), nullable=False),
        sa.Column("codigo", sa.String(length=100), nullable=True),
        sa.Column("nome", sa.String(length=255), nullable=True),
        sa.Column(
            "metadados",
            postgresql.JSONB(),
            server_default=sa.text("'{}'::jsonb"),
            nullable=False,
        ),
        sa.Column(
            "geom",
            Geometry(geometry_type="MULTIPOLYGON",
                     srid=4674, spatial_index=False),
            nullable=False,
        ),
        sa.Column(
            "imported_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.create_index("ix_restricoes_tipo", "restricoes", ["tipo"])
    op.create_index("ix_restricoes_fonte", "restricoes", ["fonte"])
    op.create_index(
        "ix_restricoes_geom", "restricoes", ["geom"], postgresql_using="gist"
    )


def downgrade() -> None:
    """Remove a tabela (os índices caem junto)."""
    op.drop_table("restricoes")
