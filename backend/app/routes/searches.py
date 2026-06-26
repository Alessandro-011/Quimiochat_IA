"""
routes/searches.py
==================
Rotas para histórico e gestão de pesquisas (protegidas por JWT).

Endpoints:
    GET /search/history  — Histórico de pesquisas do usuário autenticado

TCC - Sistema de Quimioinformática Inteligente
"""

from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.middleware.jwt_auth import get_current_user
from app.models.user import User
from app.schemas.search_schema import SearchHistoryItem
from app.controllers.search_controller import get_search_history

router = APIRouter(
    prefix="/search",
    tags=["Histórico de Pesquisas"],
)


@router.get(
    "/history",
    response_model=List[SearchHistoryItem],
    summary="Histórico de pesquisas",
    description=(
        "Retorna todas as pesquisas realizadas pelo usuário autenticado, "
        "incluindo resultados da IA e do PubChem, ordenadas da mais recente para a mais antiga."
    ),
)
def route_get_history(
    skip:         int = Query(0,  ge=0,  description="Número de registros para pular"),
    limit:        int = Query(20, ge=1, le=100, description="Máximo de registros retornados"),
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user),
):
    """
    Retorna o histórico de pesquisas do usuário logado.

    Cada item inclui:
    - Nome da molécula pesquisada
    - Resultado da IA (nome químico, SMILES, tempo)
    - Resultado do PubChem (nome, SMILES, tempo)
    - Data/hora da pesquisa
    """
    return get_search_history(current_user, db, skip=skip, limit=limit)
