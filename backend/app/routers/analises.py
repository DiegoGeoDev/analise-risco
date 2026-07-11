from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Analise, Propriedade
from app.schemas import AnaliseOut
from app.services.analise import analisar_propriedade


router = APIRouter(
    prefix="/propriedades/{propriedade_id}/analises", tags=["analises"])


def _get_propriedade(propriedade_id: int, db: Session) -> Propriedade:
    prop = db.get(Propriedade, propriedade_id)
    if prop is None:
        raise HTTPException(
            status_code=404, detail="Propriedade não encontrada")
    return prop


@router.post("", response_model=AnaliseOut, status_code=201)
def rodar_analise(propriedade_id: int, db: Session = Depends(get_db)):
    """Roda uma nova análise e a persiste (cria um registro no histórico)."""
    prop = _get_propriedade(propriedade_id, db)
    return analisar_propriedade(db, prop)


@router.get("", response_model=list[AnaliseOut])
def historico_analises(propriedade_id: int, db: Session = Depends(get_db)):
    """Histórico de análises do imóvel, mais recente primeiro (append-only)."""
    _get_propriedade(propriedade_id, db)
    stmt = (
        select(Analise)
        .where(Analise.propriedade_id == propriedade_id)
        .order_by(Analise.created_at.desc(), Analise.id.desc())
    )
    return db.scalars(stmt).all()
