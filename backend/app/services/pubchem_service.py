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


async def query_pubchem(
    molecule_name: str,
    ai_name: Optional[str] = None,
    ai_smiles: Optional[str] = None
) -> Tuple[Optional[int], Optional[str], Optional[str], Optional[str], Optional[str], Optional[str], Optional[str], int]:
    """
    Consulta o PubChem de forma robusta.

    Fluxo de fallback para encontrar o CID:
      1. Pesquisa exata do nome original.
      2. Pesquisa sem acentos (fallback embutido).
      3. Pesquisa pelo nome retornado pela IA (IUPAC ou traduzido).
      4. Busca pelo SMILES retornado pela IA.

    Após encontrar o CID, extrai propriedades completas e garante que
    campos SMILES sejam testados corretamente.

    Returns:
        Tupla contendo: (cid, nome_comum, nome_iupac, smiles_canonico, smiles_isomerico, formula, massa, tempo_ms)
    """
    start_time = time.monotonic()
    cid = None

    # Monta a lista de tentativas para buscar o CID
    name_candidates = [molecule_name]
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

    if ai_name and ai_name.strip() and ai_name not in name_candidates:
        name_candidates.append(ai_name.strip())

    # Etapa 1: Tentar descobrir o CID via nome (com fallbacks)
    async with httpx.AsyncClient(timeout=PUBCHEM_TIMEOUT) as client:
        for candidate in name_candidates:
            encoded_name = quote(candidate, safe="")
            cid_url      = f"{PUBCHEM_BASE_URL}/compound/name/{encoded_name}/cids/JSON"
            try:
                cid_resp = await client.get(cid_url)
                if cid_resp.status_code == 200:
                    cids = cid_resp.json().get("IdentifierList", {}).get("CID", [])
                    if cids:
                        cid = cids[0]
                        logger.info(f"PubChem: CID {cid} encontrado pelo nome '{candidate}'")
                        break
            except Exception as exc:
                logger.warning(f"Erro ao buscar CID pelo nome '{candidate}': {exc}")

        # Etapa 2: Se falhou via nome, tenta via SMILES da IA
        if not cid and ai_smiles and ai_smiles.strip():
            encoded_smiles = quote(ai_smiles.strip(), safe="")
            cid_url = f"{PUBCHEM_BASE_URL}/compound/smiles/{encoded_smiles}/cids/JSON"
            try:
                cid_resp = await client.get(cid_url)
                if cid_resp.status_code == 200:
                    cids = cid_resp.json().get("IdentifierList", {}).get("CID", [])
                    if cids:
                        cid = cids[0]
                        logger.info(f"PubChem: CID {cid} encontrado via SMILES da IA")
            except Exception as exc:
                logger.warning(f"Erro ao buscar CID pelo SMILES da IA: {exc}")

        elapsed_ms = int((time.monotonic() - start_time) * 1000)

        if not cid:
            logger.warning(f"PubChem: Nenhum CID encontrado para a molécula '{molecule_name}'.")
            return None, None, None, None, None, None, None, elapsed_ms

        # Etapa 3: Obter Propriedades Oficiais
        props_url = f"{PUBCHEM_BASE_URL}/compound/cid/{cid}/property/Title,IUPACName,CanonicalSMILES,IsomericSMILES,MolecularFormula,MolecularWeight/JSON"
        try:
            props_resp = await client.get(props_url)
            props_resp.raise_for_status()
            props = props_resp.json().get("PropertyTable", {}).get("Properties", [{}])[0]
            
            nome_comum       = props.get("Title")
            nome_iupac       = props.get("IUPACName")
            
            # PubChem API mapeia IsomericSMILES para "SMILES" e CanonicalSMILES para "ConnectivitySMILES" (em algumas versões JSON)
            # Mas o mais seguro é pegar diretamente caso venham com o nome correto, ou com os fallbacks.
            smiles_canonico  = props.get("CanonicalSMILES") or props.get("ConnectivitySMILES")
            smiles_isomerico = props.get("IsomericSMILES") or props.get("SMILES")
            
            formula          = props.get("MolecularFormula")
            massa            = props.get("MolecularWeight")

            if not smiles_canonico and not smiles_isomerico:
                logger.error(f"PubChem Anomalia: CID {cid} retornou sem nenhum SMILES!")
            else:
                s_utilizado = "Canonical" if smiles_canonico else "Isomeric"
                logger.info(f"PubChem: Propriedades extraídas com sucesso. SMILES {s_utilizado} utilizado.")

            elapsed_ms = int((time.monotonic() - start_time) * 1000)
            return cid, nome_comum, nome_iupac, smiles_canonico, smiles_isomerico, formula, massa, elapsed_ms

        except Exception as exc:
            logger.error(f"Erro ao obter propriedades para o CID {cid}: {exc}")
            elapsed_ms = int((time.monotonic() - start_time) * 1000)
            return cid, None, None, None, None, None, None, elapsed_ms
