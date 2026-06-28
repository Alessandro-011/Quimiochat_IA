"""
schemas/search_schema.py
========================
Schemas Pydantic para pesquisas, resultados de IA e PubChem.

TCC - Análise e Desenvolvimento de Sistemas
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
        description="Nome popular da molécula a ser pesquisada.",
    )


# ------------------------------------------------------------------
# Resultado da IA (Ollama/Gemma2)
# ------------------------------------------------------------------
class AIResultSchema(BaseModel):
    name:    Optional[str] = None
    smiles:  Optional[str] = None
    time_ms: Optional[int] = None

    model_config = {"from_attributes": True}


# ------------------------------------------------------------------
# Resultado da API PubChem
# ------------------------------------------------------------------
class PubChemResultSchema(BaseModel):
    cid:              Optional[int] = None
    nome_comum:       Optional[str] = None
    nome_iupac:       Optional[str] = None
    smiles_canonico:  Optional[str] = None
    smiles_isomerico: Optional[str] = None
    formula:          Optional[str] = None
    massa:            Optional[str] = None
    time_ms:          Optional[int] = None   # Mapeado de tempo_resposta

    model_config = {"from_attributes": True}


# ------------------------------------------------------------------
# Resposta completa de uma pesquisa
# ------------------------------------------------------------------
class SearchResponse(BaseModel):
    molecule: str
    ai:       AIResultSchema
    pubchem:  PubChemResultSchema
    search_id: Optional[int] = None


# ------------------------------------------------------------------
# Item de histórico de pesquisa (para GET /search/history)
# ------------------------------------------------------------------
class SearchHistoryItem(BaseModel):
    id:               int
    search_time:      Optional[datetime] = None
    response_time_ms: Optional[int]      = None
    molecule:         Optional[str]      = None
    
    ai_name:          Optional[str]      = None
    ai_smiles:        Optional[str]      = None
    ai_time_ms:       Optional[int]      = None
    pubchem_cid:               Optional[int] = None
    pubchem_nome_comum:        Optional[str] = None
    pubchem_nome_iupac:        Optional[str] = None
    pubchem_smiles_canonico:   Optional[str] = None
    pubchem_smiles_isomerico:  Optional[str] = None
    pubchem_formula:           Optional[str] = None
    pubchem_massa:             Optional[str] = None
    pubchem_time_ms:           Optional[int] = None

    model_config = {"from_attributes": True}
