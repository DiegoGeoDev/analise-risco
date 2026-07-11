from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models import Analise, Propriedade

# Versão da regra — gravada em cada análise para reprodutibilidade/auditoria.
VERSAO_ALGORITMO = "v1"

# Limiar anti-sliver: ignora interseções < 100 m² (ruído topológico de fronteira).
LIMIAR_SLIVER_HA = 0.01

# SQL 1: interseções relevantes (acima do limiar), para explicar o score.
_SQL_FATORES = text(
    """
    WITH imovel AS (SELECT geom FROM propriedades WHERE id = :pid)
    SELECT r.id AS restricao_id, r.tipo, r.fonte, r.codigo,
           ST_Area(ST_Intersection(i.geom, r.geom)::geography) / 10000.0 AS area_ha
    FROM imovel i
    JOIN restricoes r ON ST_Intersects(i.geom, r.geom)
    WHERE ST_Area(ST_Intersection(i.geom, r.geom)::geography) / 10000.0 > :lim
    ORDER BY area_ha DESC
    """
)

# SQL 2: área afetada TOTAL via união (evita dupla contagem se restrições se
# sobrepõem entre si). Slivers contribuem ~0, então não distorcem.
_SQL_AREA_TOTAL = text(
    """
    WITH imovel AS (SELECT geom FROM propriedades WHERE id = :pid)
    SELECT COALESCE(
        ST_Area(ST_Union(ST_Intersection(i.geom, r.geom))::geography) / 10000.0, 0
    )
    FROM imovel i
    JOIN restricoes r ON ST_Intersects(i.geom, r.geom)
    """
)


def _classificar(pct_afetado: float, tem_sobreposicao: bool) -> tuple[float, str]:
    """Traduz % afetado em score 0–100 e nível — regra v1."""
    if not tem_sobreposicao:
        return 0.0, "BAIXO"
    # piso 50 p/ presença de embargo
    score = min(100.0, 50.0 + 0.5 * pct_afetado)
    nivel = "ALTO" if score >= 70.0 else "MEDIO"
    return round(score, 2), nivel


def analisar_propriedade(db: Session, propriedade: Propriedade) -> Analise:
    """Roda a análise, persiste (append-only) e devolve o resultado."""
    linhas = db.execute(
        _SQL_FATORES, {"pid": propriedade.id, "lim": LIMIAR_SLIVER_HA}
    ).mappings().all()

    area_afetada = float(
        db.execute(_SQL_AREA_TOTAL, {"pid": propriedade.id}).scalar() or 0.0
    )

    area_imovel = float(propriedade.area_ha or 0.0)
    pct = (area_afetada / area_imovel * 100.0) if area_imovel > 0 else 0.0
    score, nivel = _classificar(pct, tem_sobreposicao=len(linhas) > 0)

    fatores = {
        "versao": VERSAO_ALGORITMO,
        "criterio": f"área de interseção > {LIMIAR_SLIVER_HA} ha (ignora slivers)",
        "area_imovel_ha": round(area_imovel, 4),
        "pct_afetado": round(pct, 2),
        "restricoes": [
            {
                "restricao_id": ln["restricao_id"],
                "tipo": ln["tipo"],
                "fonte": ln["fonte"],
                "codigo": ln["codigo"],
                "area_intersec_ha": round(float(ln["area_ha"]), 4),
                "pct_imovel": round(float(ln["area_ha"]) / area_imovel * 100.0, 2)
                if area_imovel > 0
                else 0.0,
            }
            for ln in linhas
        ],
    }

    analise = Analise(
        propriedade_id=propriedade.id,
        score=score,
        nivel_risco=nivel,
        area_afetada_ha=round(area_afetada, 4),
        fatores=fatores,
        versao_algoritmo=VERSAO_ALGORITMO,
    )
    db.add(analise)
    db.commit()
    db.refresh(analise)
    return analise
