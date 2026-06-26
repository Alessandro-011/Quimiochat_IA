"""
services/ollama_service.py
Integração com Ollama (Gemma2) para tradução de nomes e geração de SMILES.
"""

import os
import re
import json
import time
import logging
from typing import Optional, Tuple

import httpx
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL    = os.getenv("OLLAMA_MODEL",    "gemma2")
OLLAMA_TIMEOUT  = int(os.getenv("OLLAMA_TIMEOUT", "120"))

MOLECULE_PROMPT_TEMPLATE = """Você é um especialista em química e quimioinformática.

O usuário forneceu o seguinte nome de molécula: "{molecule_name}"

Sua tarefa é:
1. Identificar a molécula correta (pode ser nome popular, em português ou inglês).
2. Fornecer a nomenclatura química internacional (IUPAC ou nome comum reconhecido internacionalmente).
3. Gerar a representação SMILES (Simplified Molecular Input Line Entry System) correta e válida.

Responda SOMENTE com um JSON válido, sem explicações adicionais, no seguinte formato exato:
{{
  "nome_quimico": "Nome químico internacional aqui",
  "smiles": "SMILES aqui",
  "confianca": "alta/media/baixa"
}}

Não inclua nenhum texto antes ou depois do JSON."""


async def query_ollama(molecule_name: str) -> Tuple[Optional[str], Optional[str], int]:
    """
    Envia o nome da molécula ao Gemma2 e extrai nome químico + SMILES do JSON retornado.
    Retorna (nome_quimico, smiles, tempo_ms). Campos podem ser None em falha.
    """
    prompt     = MOLECULE_PROMPT_TEMPLATE.format(molecule_name=molecule_name)
    start_time = time.monotonic()

    try:
        async with httpx.AsyncClient(timeout=OLLAMA_TIMEOUT) as client:
            response = await client.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={
                    "model":  OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.1, "top_p": 0.9},
                },
            )
            response.raise_for_status()
    except httpx.ConnectError:
        elapsed_ms = int((time.monotonic() - start_time) * 1000)
        logger.error("Ollama não está em execução em %s", OLLAMA_BASE_URL)
        return None, None, elapsed_ms
    except httpx.TimeoutException:
        elapsed_ms = int((time.monotonic() - start_time) * 1000)
        logger.error("Timeout ao consultar Ollama após %ds", OLLAMA_TIMEOUT)
        return None, None, elapsed_ms
    except httpx.HTTPStatusError as exc:
        elapsed_ms = int((time.monotonic() - start_time) * 1000)
        logger.error("Erro HTTP Ollama: %s", exc)
        return None, None, elapsed_ms

    elapsed_ms = int((time.monotonic() - start_time) * 1000)

    try:
        data      = response.json()
        raw_text  = data.get("response", "")
        # Extrai o primeiro bloco JSON mesmo que o modelo inclua texto extra
        json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        if json_match:
            parsed       = json.loads(json_match.group())
            nome_quimico = parsed.get("nome_quimico") or parsed.get("nome") or None
            smiles       = parsed.get("smiles") or None
            return nome_quimico, smiles, elapsed_ms
    except (json.JSONDecodeError, KeyError, AttributeError) as exc:
        logger.error("Erro ao parsear resposta Ollama: %s", exc)

    return None, None, elapsed_ms


async def check_ollama_health() -> bool:
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
            return resp.status_code == 200
    except Exception:
        return False
