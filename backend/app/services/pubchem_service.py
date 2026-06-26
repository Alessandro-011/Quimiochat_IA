"""
services/pubchem_service.py
Serviço de integração com a API pública PubChem (PUG REST).

A URL é construída com urllib.parse.quote para codificar corretamente
nomes em português (acentos, espaços etc.) antes de enviar à API.
"""

import time
import logging
from typing import Optional, Tuple
from urllib.parse import quote

import httpx

logger = logging.getLogger(__name__)

PUBCHEM_BASE_URL = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
PUBCHEM_TIMEOUT  = 20


async def query_pubchem(molecule_name: str) -> Tuple[Optional[int], Optional[str], Optional[str], int]:
    """
    Consulta o PubChem pelo nome da molécula em duas etapas:
      1. Resolve nome → CID (aceita nomes em PT/EN)
      2. Busca IUPACName + CanonicalSMILES pelo CID

    Retorna (cid, nome_iupac, smiles, tempo_ms). Campos podem ser None em falha.
    """
    start_time = time.monotonic()

    # Tenta primeiro com o nome original, depois sem acentos como fallback
    candidates = [molecule_name]
    try:
        import unicodedata
        sem_acento = "".join(
            c for c in unicodedata.normalize("NFD", molecule_name)
            if unicodedata.category(c) != "Mn"
        )
        if sem_acento != molecule_name:
            candidates.append(sem_acento)
    except Exception:
        pass

    cid = None
    for candidate in candidates:
        encoded_name = quote(candidate, safe="")
        cid_url      = f"{PUBCHEM_BASE_URL}/compound/name/{encoded_name}/cids/JSON"
        try:
            async with httpx.AsyncClient(timeout=PUBCHEM_TIMEOUT) as client:
                cid_resp = await client.get(cid_url)
                if cid_resp.status_code == 200:
                    cid_data = cid_resp.json()
                    cids     = cid_data.get("IdentifierList", {}).get("CID", [])
                    if cids:
                        cid = cids[0]
                        break
        except (httpx.ConnectError, httpx.TimeoutException):
            elapsed_ms = int((time.monotonic() - start_time) * 1000)
            logger.warning("PubChem inacessível após %.0f ms", elapsed_ms)
            return None, None, None, elapsed_ms
        except Exception as exc:
            logger.error("Erro inesperado na busca PubChem CID: %s", exc)

    elapsed_ms = int((time.monotonic() - start_time) * 1000)

    if not cid:
        logger.warning("PubChem: nenhum CID encontrado para '%s'", molecule_name)
        return None, None, None, elapsed_ms

    # Etapa 2 — busca propriedades pelo CID
    props_url = f"{PUBCHEM_BASE_URL}/compound/cid/{cid}/property/IUPACName,CanonicalSMILES/JSON"
    try:
        async with httpx.AsyncClient(timeout=PUBCHEM_TIMEOUT) as client:
            props_resp = await client.get(props_url)
            props_resp.raise_for_status()
            props_data = props_resp.json()
            props      = props_data.get("PropertyTable", {}).get("Properties", [{}])[0]
            nome_iupac = props.get("IUPACName")
            smiles     = props.get("CanonicalSMILES")
    except (httpx.ConnectError, httpx.TimeoutException):
        logger.warning("PubChem timeout ao buscar propriedades do CID %d", cid)
        return cid, None, None, int((time.monotonic() - start_time) * 1000)
    except Exception as exc:
        logger.error("Erro ao buscar propriedades PubChem CID %d: %s", cid, exc)
        return cid, None, None, int((time.monotonic() - start_time) * 1000)

    elapsed_ms = int((time.monotonic() - start_time) * 1000)
    return cid, nome_iupac, smiles, elapsed_ms
