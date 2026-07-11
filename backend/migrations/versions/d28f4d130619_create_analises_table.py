"""create analises table

Revision ID: d28f4d130619
Revises: 7322b418c865
Create Date: 2026-07-11 17:53:21.353952

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'd28f4d130619'
down_revision: Union[str, Sequence[str], None] = '7322b418c865'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Cria a tabela de resultados de análise (append-only, auditável)."""
    op.create_table(
        "analises",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("propriedade_id", sa.BigInteger(), nullable=False),
        sa.Column("score", sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column("nivel_risco", sa.String(length=10), nullable=False),
        sa.Column(
            "area_afetada_ha",
            sa.Numeric(precision=14, scale=4),
            server_default=sa.text("0"),
            nullable=False,
        ),
        sa.Column(
            "fatores",
            postgresql.JSONB(),
            server_default=sa.text("'{}'::jsonb"),
            nullable=False,
        ),
        sa.Column("versao_algoritmo", sa.String(length=20), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(
            ["propriedade_id"], ["propriedades.id"], name="fk_analises_propriedade"
        ),

        sa.CheckConstraint(
            "nivel_risco IN ('BAIXO', 'MEDIO', 'ALTO')",
            name="ck_analises_nivel_risco",
        ),
    )
    op.create_index("ix_analises_propriedade_id",
                    "analises", ["propriedade_id"])


def downgrade() -> None:
    """Remove a tabela (índices e constraints caem junto)."""
    op.drop_table("analises")
