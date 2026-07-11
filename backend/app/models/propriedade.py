from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from geoalchemy2 import Geometry
from sqlalchemy import BigInteger, DateTime, Numeric, String, func, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

if TYPE_CHECKING:
    from app.models.analise import Analise


class Propriedade(Base):
    """Imóvel rural (CAR) — o sujeito da análise de crédito.

    Uma linha por imóvel, identificado unicamente por `cod_car` (código do
    SICAR). As partes multipolígono do shapefile são dissolvidas no ETL.
    """

    __tablename__ = "propriedades"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    # cod_car é a chave de negócio
    cod_car: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True, index=True
    )

    municipio: Mapped[str | None] = mapped_column(String(150))
    uf: Mapped[str | None] = mapped_column(String(2))

    # Área geodésica em hectares
    area_ha: Mapped[float | None] = mapped_column(Numeric(14, 4))

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

    # Lado "1" da relação 1—N: um imóvel tem várias análises (histórico).
    analises: Mapped[list[Analise]] = relationship(back_populates="propriedade")
