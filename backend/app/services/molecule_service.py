"""
services/molecule_service.py
============================
Serviço orquestrador para pesquisa de moléculas.

TCC - Sistema de Quimioinformática Inteligente
"""

import json
import logging
from sqlalchemy.orm import Session

from app.models.search_history import Search
from app.models.ai_result import AIResult
from app.models.pubchem_result import PubChemResult
from app.schemas.search_schema import SearchResponse, AIResultSchema, PubChemResultSchema
from app.services.ollama_service import query_ollama
from app.services.pubchem_service import query_pubchem

logger = logging.getLogger(__name__)


async def perform_molecule_search(molecule_name: str, user_id: int, db: Session) -> SearchResponse:
    """
    Realiza a pesquisa da molécula em sequência inteligente:
      1. Consulta a IA (Gemma2) para obter tradução e SMILES.
      2. Usa os dados da IA como fallback para a consulta ao PubChem.
    """
    logger.info("Pesquisa iniciada: '%s' para user_id=%d", molecule_name, user_id)

    # 1. Busca na IA
    ai_nome, ai_smiles, ai_tempo = await query_ollama(molecule_name)
    
    # 2. Busca no PubChem (passando fallback_smiles da IA, se houver, e a tradução ai_nome)
    (
        pc_cid, pc_nome_comum, pc_nome_iupac, pc_smiles_c, pc_smiles_i, 
        pc_formula, pc_massa, pc_tempo
    ) = await query_pubchem(molecule_name, fallback_name=ai_nome, fallback_smiles=ai_smiles)

    # Criação do objeto de resposta
    ai_schema = AIResultSchema(
        name=ai_nome,
        smiles=ai_smiles,
        time_ms=ai_tempo,
    )

    pc_schema = PubChemResultSchema(
        cid=pc_cid,
        nome_comum=pc_nome_comum,
        nome_iupac=pc_nome_iupac,
        smiles_canonico=pc_smiles_c,
        smiles_isomerico=pc_smiles_i,
        formula=pc_formula,
        massa=pc_massa,
        time_ms=pc_tempo,
    )

    response = SearchResponse(
        molecule=molecule_name,
        ai=ai_schema,
        pubchem=pc_schema,
    )

    # 3. Salvar no Banco de Dados
    try:
        from app.models.molecule import Molecule
        
        # Obter ou criar a Molécula
        molecule_record = db.query(Molecule).filter(Molecule.nome_original == molecule_name).first()
        if not molecule_record:
            molecule_record = Molecule(
                nome_original=molecule_name,
                nome_quimico=pc_nome_comum or pc_nome_iupac or ai_nome,
                smiles=pc_smiles_c or ai_smiles
            )
            db.add(molecule_record)
            db.flush()

        search_record = Search(
            user_id=user_id,
            molecule_id=molecule_record.id,
            response_time_ms=max(ai_tempo, pc_tempo) if ai_tempo and pc_tempo else 0
        )
        db.add(search_record)
        db.flush()

        ai_json_str = json.dumps({"nome": ai_nome, "smiles": ai_smiles}) if (ai_nome or ai_smiles) else None
        
        ai_record = AIResult(
            search_id=search_record.id,
            modelo="gemma2",
            resultado=ai_json_str,
            tempo_resposta=ai_tempo
        )
        db.add(ai_record)

        pc_record = PubChemResult(
            search_id=search_record.id,
            cid=pc_cid,
            nome_comum=pc_nome_comum,
            nome_iupac=pc_nome_iupac,
            smiles_canonico=pc_smiles_c,
            smiles_isomerico=pc_smiles_i,
            formula=pc_formula,
            massa=pc_massa,
            tempo_resposta=pc_tempo
        )
        db.add(pc_record)

        db.commit()
        response.search_id = search_record.id
        logger.info("Pesquisa salva no BD: id=%d | AI=%dms | PubChem=%dms", search_record.id, ai_tempo or 0, pc_tempo)

    except Exception as exc:
        db.rollback()
        logger.error("Erro ao salvar pesquisa no BD: %s", exc)

    return response
