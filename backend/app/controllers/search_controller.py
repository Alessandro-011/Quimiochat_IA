"""
controllers/search_controller.py
=================================
Lógica de negócio para pesquisa de moléculas e histórico.

TCC - Sistema de Quimioinformática Inteligente
"""

import json
import logging
from typing import List

from sqlalchemy.orm import Session, joinedload

from app.models.search_history import Search
from app.models.user import User
from app.schemas.search_schema import SearchRequest, SearchResponse, SearchHistoryItem
from app.services.molecule_service import perform_molecule_search

logger = logging.getLogger(__name__)


async def search_molecule(
    request: SearchRequest,
    current_user: User,
    db: Session,
) -> SearchResponse:
    """
    Ponto de entrada para pesquisa de molécula.
    Delega ao molecule_service que orquestra IA + PubChem em paralelo.

    Args:
        request     : SearchRequest com o nome da molécula.
        current_user: Usuário autenticado (JWT).
        db          : Sessão do banco.

    Returns:
        SearchResponse com comparativo AI vs PubChem.
    """
    logger.info(
        "Pesquisa iniciada por user_id=%d: '%s'",
        current_user.id,
        request.molecule_name,
    )
    result = await perform_molecule_search(
        molecule_name = request.molecule_name,
        user_id       = current_user.id,
        db            = db,
    )
    return result


def get_search_history(
    current_user: User,
    db: Session,
    skip: int = 0,
    limit: int = 20,
) -> List[SearchHistoryItem]:
    """
    Retorna o histórico de pesquisas do usuário autenticado.

    Args:
        current_user: Usuário autenticado.
        db          : Sessão do banco.
        skip        : Offset para paginação.
        limit       : Máximo de registros.

    Returns:
        Lista de SearchHistoryItem com dados enriquecidos.
    """
    searches = (
        db.query(Search)
        .options(
            joinedload(Search.molecule),
            joinedload(Search.ai_result),
            joinedload(Search.pubchem_result),
        )
        .filter(Search.user_id == current_user.id)
        .order_by(Search.search_time.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    history = []
    for s in searches:
        # Parseia o JSON de resultado da IA
        ai_nome  = None
        ai_smiles = None
        if s.ai_result and s.ai_result.resultado:
            try:
                ai_data  = json.loads(s.ai_result.resultado)
                ai_nome  = ai_data.get("nome")
                ai_smiles = ai_data.get("smiles")
            except (json.JSONDecodeError, AttributeError):
                pass

        item = SearchHistoryItem(
            id               = s.id,
            search_time      = s.search_time,
            response_time_ms = s.response_time_ms,
            molecule         = s.molecule.nome_original if s.molecule else None,
            ai_name          = ai_nome,
            ai_smiles        = ai_smiles,
            ai_time_ms       = s.ai_result.tempo_resposta    if s.ai_result    else None,
            pubchem_cid              = s.pubchem_result.cid             if s.pubchem_result else None,
            pubchem_nome_comum       = s.pubchem_result.nome_comum      if s.pubchem_result else None,
            pubchem_nome_iupac       = s.pubchem_result.nome_iupac      if s.pubchem_result else None,
            pubchem_smiles_canonico  = s.pubchem_result.smiles_canonico if s.pubchem_result else None,
            pubchem_smiles_isomerico = s.pubchem_result.smiles_isomerico if s.pubchem_result else None,
            pubchem_formula          = s.pubchem_result.formula         if s.pubchem_result else None,
            pubchem_massa            = s.pubchem_result.massa           if s.pubchem_result else None,
            pubchem_time_ms          = s.pubchem_result.tempo_resposta  if s.pubchem_result else None,
        )
        history.append(item)

    return history
