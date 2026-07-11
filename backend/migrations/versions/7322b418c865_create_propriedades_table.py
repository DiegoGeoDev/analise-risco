"""create propriedades table

Revision ID: 7322b418c865
Revises: f3077f6b0e06
Create Date: 2026-07-11 17:06:02.297147

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from geoalchemy2 import Geometry


# revision identifiers, used by Alembic.
revision: str = '7322b418c865'
down_revision: Union[str, Sequence[str], None] = 'f3077f6b0e06'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Cria a tabela de imóveis rurais (CAR)."""
    op.create_table(
        "propriedades",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("cod_car", sa.String(length=100), nullable=False),
        sa.Column("municipio", sa.String(length=150), nullable=True),
        sa.Column("uf", sa.String(length=2), nullable=True),
        sa.Column("area_ha", sa.Numeric(precision=14, scale=4), nullable=True),
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
    # cod_car é a chave de negócio
    op.create_index(
        "ix_propriedades_cod_car", "propriedades", ["cod_car"], unique=True
    )
    op.create_index(
        "ix_propriedades_geom", "propriedades", ["geom"], postgresql_using="gist"
    )


def downgrade() -> None:
    """Remove a tabela (os índices caem junto)."""
    op.drop_table("propriedades")
