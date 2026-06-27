"""
services/molecule_service.py
============================
Orquestrador de pesquisa molecular.
Executa a IA (Gemma2) primeiro para gerar inteligência, e então repassa os
dados da IA como fallbacks para a busca rigorosa no PubChem.

TCC - Análise e Desenvolvimento de Sistemas
"""

import json
import logging
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
    Busca de molécula com arquitetura de fallback:
    1. Executa IA.
    2. Executa PubChem passando os dados da IA como fallback.
    """
    logger.info("Pesquisa iniciada: '%s' para user_id=%d", molecule_name, user_id)

    # 1. Executa a IA primeiro (para obter traduções/IUPAC/SMILES de fallback)
    ai_nome, ai_smiles, ai_time_ms = await query_ollama(molecule_name)

    # 2. Executa o PubChem usando os dados da IA como fallback de busca
    (
        pc_cid, pc_nome_comum, pc_nome_iupac,
        pc_smiles_canonico, pc_smiles_isomerico,
        pc_formula, pc_massa, pc_time_ms
    ) = await query_pubchem(molecule_name, ai_name=ai_nome, ai_smiles=ai_smiles)

    total_time_ms = (ai_time_ms or 0) + (pc_time_ms or 0)

    # Resolve o nome e o SMILES para a tabela geral `molecules`
    nome_quimico_final = pc_nome_comum or pc_nome_iupac or ai_nome
    smiles_final       = pc_smiles_canonico or pc_smiles_isomerico or ai_smiles

    # Persiste na tabela Molecules
    molecule = _get_or_create_molecule(db, molecule_name, nome_quimico_final, smiles_final)

    # Persiste o histórico
    search = Search(
        user_id          = user_id,
        molecule_id      = molecule.id,
        response_time_ms = total_time_ms,
    )
    db.add(search)
    db.flush()

    # Persiste resultado IA
    db.add(AIResult(
        search_id      = search.id,
        modelo         = "gemma2",
        resultado      = json.dumps({"nome": ai_nome, "smiles": ai_smiles}, ensure_ascii=False),
        tempo_resposta = ai_time_ms,
    ))

    # Persiste resultado PubChem (agora com campos precisos e separados)
    db.add(PubChemResult(
        search_id        = search.id,
        cid              = pc_cid,
        nome_comum       = pc_nome_comum,
        nome_iupac       = pc_nome_iupac,
        smiles_canonico  = pc_smiles_canonico,
        smiles_isomerico = pc_smiles_isomerico,
        formula          = pc_formula,
        massa            = pc_massa,
        tempo_resposta   = pc_time_ms,
    ))

    db.commit()
    db.refresh(search)

    logger.info("Pesquisa salva no BD: id=%d | AI=%dms | PubChem=%dms",
                search.id, ai_time_ms or 0, pc_time_ms or 0)

    return SearchResponse(
        molecule  = molecule_name,
        search_id = search.id,
        ai        = AIResultSchema(name=ai_nome, smiles=ai_smiles, time_ms=ai_time_ms),
        pubchem   = PubChemResultSchema(
            cid              = pc_cid,
            nome_comum       = pc_nome_comum,
            nome_iupac       = pc_nome_iupac,
            smiles_canonico  = pc_smiles_canonico,
            smiles_isomerico = pc_smiles_isomerico,
            formula          = pc_formula,
            massa            = pc_massa,
            time_ms          = pc_time_ms,
        ),
    )


def _get_or_create_molecule(
    db: Session,
    nome_original: str,
    nome_quimico: Optional[str],
    smiles: Optional[str],
) -> Molecule:
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
