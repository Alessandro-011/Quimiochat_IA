"""
schemas/search_schema.py
========================
Schemas Pydantic para pesquisas, resultados de IA e PubChem.

TCC - Sistema de Quimioinformática Inteligente
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


# ------------------------------------------------------------------
# Schema de entrada — pesquisa de molécula pelo usuário
# ------------------------------------------------------------------
class SearchRequest(BaseModel):
    molecule_name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        examples=["Aspirina"],
        description="Nome popular da molécula a ser pesquisada (em português).",
    )


# ------------------------------------------------------------------
# Resultado da IA (Ollama/Gemma2)
# ------------------------------------------------------------------
class AIResultSchema(BaseModel):
    name:    Optional[str] = None   # Nome químico retornado pela IA
    smiles:  Optional[str] = None   # SMILES gerado pela IA
    time_ms: Optional[int] = None   # Tempo de resposta em ms

    model_config = {"from_attributes": True}


# ------------------------------------------------------------------
# Resultado da API PubChem
# ------------------------------------------------------------------
class PubChemResultSchema(BaseModel):
    cid:     Optional[int] = None   # PubChem Compound ID
    name:    Optional[str] = None   # Nome retornado pelo PubChem
    smiles:  Optional[str] = None   # SMILES canônico
    time_ms: Optional[int] = None   # Tempo de resposta em ms

    model_config = {"from_attributes": True}


# ------------------------------------------------------------------
# Resposta completa de uma pesquisa — formato JSON especificado no TCC
# ------------------------------------------------------------------
class SearchResponse(BaseModel):
    molecule: str                        # Nome pesquisado
    ai:       AIResultSchema             # Dados da IA
    pubchem:  PubChemResultSchema        # Dados do PubChem
    search_id: Optional[int] = None     # ID do registro no banco


# ------------------------------------------------------------------
# Item de histórico de pesquisa (para GET /search/history)
# ------------------------------------------------------------------
class SearchHistoryItem(BaseModel):
    id:               int
    search_time:      Optional[datetime] = None
    response_time_ms: Optional[int]      = None
    molecule:         Optional[str]      = None   # nome_original
    ai_name:          Optional[str]      = None
    ai_smiles:        Optional[str]      = None
    ai_time_ms:       Optional[int]      = None
    pubchem_name:     Optional[str]      = None
    pubchem_smiles:   Optional[str]      = None
    pubchem_time_ms:  Optional[int]      = None

    model_config = {"from_attributes": True}
