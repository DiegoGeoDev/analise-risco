from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

if TYPE_CHECKING:
    from app.models.propriedade import Propriedade


class Analise(Base):
    """Resultado de UMA execução de análise de risco sobre um imóvel.

    Append-only: cada análise é um registro novo (nunca UPDATE), formando o
    histórico auditável. `fatores` guarda a explicabilidade (quais restrições
    e quanto pesaram) e `versao_algoritmo` permite reproduzir a lógica usada.
    """

    __tablename__ = "analises"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    propriedade_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("propriedades.id"), nullable=False, index=True
    )

    score: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    nivel_risco: Mapped[str] = mapped_column(String(10), nullable=False)
    area_afetada_ha: Mapped[float] = mapped_column(
        Numeric(14, 4), nullable=False, server_default=text("0")
    )

    fatores: Mapped[dict] = mapped_column(
        JSONB, nullable=False, server_default=text("'{}'::jsonb")
    )
    versao_algoritmo: Mapped[str] = mapped_column(String(20), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    propriedade: Mapped[Propriedade] = relationship(back_populates="analises")
