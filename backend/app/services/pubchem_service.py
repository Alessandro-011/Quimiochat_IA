"""
services/pubchem_service.py
===========================
Serviço de integração com a API pública PubChem (PUG REST).
Implementa busca multietapa e fallbacks robustos para extração rigorosa
de propriedades (Title, IUPACName, SMILES, Fórmula e Massa).

TCC - Análise e Desenvolvimento de Sistemas
"""

import time
import logging
from typing import Optional, Tuple
from urllib.parse import quote

import httpx

logger = logging.getLogger(__name__)

PUBCHEM_BASE_URL = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
PUBCHEM_TIMEOUT  = 20


async def query_pubchem(molecule_name: str, fallback_name: str = None, fallback_smiles: str = None) -> Tuple[Optional[int], Optional[str], Optional[str], Optional[str], Optional[str], Optional[str], Optional[str], int]:
    """
    Consulta o PubChem pelo nome da molécula em múltiplas etapas:
      1. Resolve nome -> CID (com suporte a fallback em inglês/SMILES via IA).
      2. Busca propriedades rigorosas pelo CID.

    Retorna (cid, nome_comum, nome_iupac, smiles_canonico, smiles_isomerico, formula, massa, tempo_ms).
    """
    start_time = time.monotonic()
    cid = None

    candidates = [molecule_name]
    if fallback_name and fallback_name.strip() and fallback_name.strip().lower() != molecule_name.lower():
        candidates.append(fallback_name.strip())
    
    # Adiciona versão sem acentos
    try:
        import unicodedata
        sem_acento = "".join(
            c for c in unicodedata.normalize("NFD", molecule_name)
            if unicodedata.category(c) != "Mn"
        )
        if sem_acento != molecule_name:
            name_candidates.append(sem_acento)
    except Exception:
        pass

    cid = None
    
    # 1. Tentar por Nome
    for candidate in candidates:
        if not candidate: continue
        encoded_name = quote(candidate, safe="")
        cid_url = f"{PUBCHEM_BASE_URL}/compound/name/{encoded_name}/cids/JSON"
        try:
            async with httpx.AsyncClient(timeout=PUBCHEM_TIMEOUT) as client:
                cid_resp = await client.get(cid_url)
                if cid_resp.status_code == 200:
                    cid_data = cid_resp.json()
                    cids = cid_data.get("IdentifierList", {}).get("CID", [])
                    if cids:
                        cid = cids[0]
                        logger.info("PubChem: CID %d encontrado pelo nome '%s'", cid, candidate)
                        break
        except Exception as exc:
            logger.error("Erro ao buscar CID pelo nome '%s': %s", candidate, exc)

    # 2. Fallback: Tentar por SMILES estrutural (Reverso)
    if not cid and fallback_smiles:
        encoded_smiles = quote(fallback_smiles, safe="")
        smiles_url = f"{PUBCHEM_BASE_URL}/compound/smiles/{encoded_smiles}/cids/JSON"
        try:
            async with httpx.AsyncClient(timeout=PUBCHEM_TIMEOUT) as client:
                smiles_resp = await client.get(smiles_url)
                if smiles_resp.status_code == 200:
                    smiles_data = smiles_resp.json()
                    cids = smiles_data.get("IdentifierList", {}).get("CID", [])
                    if cids:
                        cid = cids[0]
                        logger.info("PubChem: CID %d encontrado via fallback SMILES", cid)
        except Exception as exc:
            logger.error("Erro ao buscar CID pelo SMILES: %s", exc)

    if not cid:
        logger.warning("PubChem: nenhum CID encontrado para '%s'", molecule_name)
        return None, None, None, None, None, None, None, int((time.monotonic() - start_time) * 1000)

    # Etapa 3 — Busca de Propriedades Rigorosas pelo CID
    props_url = f"{PUBCHEM_BASE_URL}/compound/cid/{cid}/property/Title,IUPACName,CanonicalSMILES,IsomericSMILES,MolecularFormula,MolecularWeight/JSON"
    
    nome_comum = None
    nome_iupac = None
    smiles_c = None
    smiles_i = None
    formula = None
    massa = None
    
    try:
        async with httpx.AsyncClient(timeout=PUBCHEM_TIMEOUT) as client:
            props_resp = await client.get(props_url)
            if props_resp.status_code == 200:
                props_data = props_resp.json()
                props = props_data.get("PropertyTable", {}).get("Properties", [{}])[0]
                
                nome_comum = props.get("Title")
                nome_iupac = props.get("IUPACName")
                smiles_c   = props.get("CanonicalSMILES")
                smiles_i   = props.get("IsomericSMILES")
                formula    = props.get("MolecularFormula")
                massa      = props.get("MolecularWeight")
                
                # Alguns CIDs não têm CanonicalSMILES no JSON padrão de propriedade, ou usam outras chaves
                if not smiles_c and props.get("ConnectivitySMILES"):
                    smiles_c = props.get("ConnectivitySMILES")
                if not smiles_c and props.get("SMILES"):
                    smiles_c = props.get("SMILES")

    except Exception as exc:
        logger.error("Erro ao buscar propriedades PubChem CID %d: %s", cid, exc)

    elapsed_ms = int((time.monotonic() - start_time) * 1000)
    return cid, nome_comum, nome_iupac, smiles_c, smiles_i, formula, massa, elapsed_ms
