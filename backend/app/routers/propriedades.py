from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Propriedade
from app.schemas import PropriedadeOut


router = APIRouter(prefix="/propriedades", tags=["propriedades"])


@router.get("", response_model=list[PropriedadeOut])
def listar_propriedades(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    """Lista imóveis paginados (atributos; a geometria virá via tiles Martin)."""
    stmt = (
        select(Propriedade)
        .order_by(Propriedade.id)
        .limit(limit)
        .offset(offset)
    )
    return db.scalars(stmt).all()
