"""
controllers/search_controller.py
=================================
Lógica de negócio para pesquisa de moléculas e histórico.

TCC - Análise e Desenvolvimento de Sistemas
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
        ai_nome  = None
        ai_smiles = None
        if s.ai_result and s.ai_result.resultado:
            try:
                ai_data  = json.loads(s.ai_result.resultado)
                ai_nome  = ai_data.get("nome")
                ai_smiles = ai_data.get("smiles")
            except (json.JSONDecodeError, AttributeError):
                pass

        pc = s.pubchem_result

        item = SearchHistoryItem(
            id               = s.id,
            search_time      = s.search_time,
            response_time_ms = s.response_time_ms,
            molecule         = s.molecule.nome_original if s.molecule else None,
            
            ai_name          = ai_nome,
            ai_smiles        = ai_smiles,
            ai_time_ms       = s.ai_result.tempo_resposta if s.ai_result else None,
            
            pubchem_cid             = pc.cid if pc else None,
            pubchem_nome_comum      = pc.nome_comum if pc else None,
            pubchem_nome_iupac      = pc.nome_iupac if pc else None,
            pubchem_smiles_canonico = pc.smiles_canonico if pc else None,
            pubchem_smiles_isomerico= pc.smiles_isomerico if pc else None,
            pubchem_formula         = pc.formula if pc else None,
            pubchem_massa           = pc.massa if pc else None,
            pubchem_time_ms         = pc.tempo_resposta if pc else None,
        )
        history.append(item)

    return history
