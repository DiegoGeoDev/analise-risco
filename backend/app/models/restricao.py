from datetime import datetime

from geoalchemy2 import Geometry
from sqlalchemy import BigInteger, DateTime, String, func, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Restricao(Base):
    """Restrição ambiental que pode incidir sobre um imóvel rural.

    Tabela única e genérica: `tipo` discrimina a natureza (embargo, UC, TI...)
    e `metadados` (JSONB) absorve os atributos específicos de cada tipo, sem
    exigir mudança de schema quando um tipo novo entrar.
    """

    __tablename__ = "restricoes"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    tipo: Mapped[str] = mapped_column(String(50), index=True)
    fonte: Mapped[str] = mapped_column(String(50), index=True)

    codigo: Mapped[str | None] = mapped_column(String(100))
    nome: Mapped[str | None] = mapped_column(String(255))

    metadados: Mapped[dict] = mapped_column(
        JSONB, nullable=False, server_default=text("'{}'::jsonb")
    )

    geom: Mapped[str] = mapped_column(
        Geometry(geometry_type="MULTIPOLYGON", srid=4674, spatial_index=False),
        nullable=False,
    )

    imported_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
