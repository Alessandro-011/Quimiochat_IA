"""
services/molecule_service.py
Orquestrador de pesquisa molecular: dispara Ollama e PubChem em paralelo,
persiste os resultados e retorna o JSON comparativo.
"""

import json
import logging
import asyncio
from typing import Optional

from sqlalchemy.orm import Session

from app.models.molecule import Molecule
from app.models.search_history import Search
from app.models.ai_result import AIResult
from app.models.pubchem_result import PubChemResult
from app.schemas.search_schema import SearchResponse, AIResultSchema, PubChemResultSchema
from app.services.ollama_service import query_ollama
from app.services.pubchem_service import query_pubchem

logger = logging.getLogger(__name__)


async def perform_molecule_search(
    molecule_name: str,
    user_id: int,
    db: Session,
) -> SearchResponse:
    """
    Dispara consultas simultâneas (asyncio.gather) ao Ollama e ao PubChem,
    salva tudo no banco em um único commit e retorna o comparativo.
    """
    logger.info("Pesquisa: '%s' para user_id=%d", molecule_name, user_id)

    (ai_nome, ai_smiles, ai_time_ms), \
    (pc_cid, pc_nome, pc_smiles, pc_time_ms) = await asyncio.gather(
        query_ollama(molecule_name),
        query_pubchem(molecule_name),
    )

    total_time_ms = max(ai_time_ms or 0, pc_time_ms or 0)

    nome_quimico_final = pc_nome or ai_nome
    smiles_final       = pc_smiles or ai_smiles

    molecule = _get_or_create_molecule(db, molecule_name, nome_quimico_final, smiles_final)

    search = Search(
        user_id          = user_id,
        molecule_id      = molecule.id,
        response_time_ms = total_time_ms,
    )
    db.add(search)
    db.flush()

    db.add(AIResult(
        search_id      = search.id,
        modelo         = "gemma2",
        resultado      = json.dumps({"nome": ai_nome, "smiles": ai_smiles}, ensure_ascii=False),
        tempo_resposta = ai_time_ms,
    ))

    db.add(PubChemResult(
        search_id      = search.id,
        cid            = pc_cid,
        nome           = pc_nome,
        smiles         = pc_smiles,
        tempo_resposta = pc_time_ms,
    ))

    db.commit()
    db.refresh(search)

    logger.info("Pesquisa salva: id=%d | AI=%dms | PubChem=%dms",
                search.id, ai_time_ms or 0, pc_time_ms or 0)

    return SearchResponse(
        molecule  = molecule_name,
        search_id = search.id,
        ai        = AIResultSchema(name=ai_nome, smiles=ai_smiles, time_ms=ai_time_ms),
        pubchem   = PubChemResultSchema(cid=pc_cid, name=pc_nome, smiles=pc_smiles, time_ms=pc_time_ms),
    )


def _get_or_create_molecule(
    db: Session,
    nome_original: str,
    nome_quimico: Optional[str],
    smiles: Optional[str],
) -> Molecule:
    """Busca molécula existente pelo nome original ou cria uma nova entrada."""
    molecule = (
        db.query(Molecule)
        .filter(Molecule.nome_original.ilike(nome_original.strip()))
        .first()
    )
    if molecule:
        if not molecule.nome_quimico and nome_quimico:
            molecule.nome_quimico = nome_quimico
        if not molecule.smiles and smiles:
            molecule.smiles = smiles
        db.flush()
        return molecule

    molecule = Molecule(
        nome_original = nome_original.strip(),
        nome_quimico  = nome_quimico,
        smiles        = smiles,
    )
    db.add(molecule)
    db.flush()
    return molecule
