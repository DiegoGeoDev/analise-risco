from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PropriedadeOut(BaseModel):
    """DTO de saída de um imóvel — controla o que a API expõe.

    from_attributes=True permite construir este schema direto de um objeto ORM
    (lê os atributos), sem conversão manual.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    cod_car: str
    municipio: str | None
    uf: str | None
    area_ha: float | None


class AnaliseOut(BaseModel):
    """DTO de saída de uma análise — o resultado explicável e auditável."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    propriedade_id: int
    score: float
    nivel_risco: str
    area_afetada_ha: float
    fatores: dict
    versao_algoritmo: str
    created_at: datetime
