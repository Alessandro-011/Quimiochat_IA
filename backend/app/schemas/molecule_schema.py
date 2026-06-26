"""
schemas/molecule_schema.py
==========================
Schemas Pydantic para validação e serialização de moléculas.

TCC - Sistema de Quimioinformática Inteligente
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


# ------------------------------------------------------------------
# Schema base — campos compartilhados
# ------------------------------------------------------------------
class MoleculeBase(BaseModel):
    nome_original: str = Field(..., min_length=1, max_length=255, examples=["Aspirina"])


# ------------------------------------------------------------------
# Schema de criação de molécula (uso interno)
# ------------------------------------------------------------------
class MoleculeCreate(MoleculeBase):
    nome_quimico: Optional[str] = Field(None, max_length=500)
    smiles:       Optional[str] = None


# ------------------------------------------------------------------
# Schema de resposta de molécula
# ------------------------------------------------------------------
class MoleculeResponse(MoleculeBase):
    id:           int
    nome_quimico: Optional[str] = None
    smiles:       Optional[str] = None
    created_at:   Optional[datetime] = None

    model_config = {"from_attributes": True}


# ------------------------------------------------------------------
# Schema simplificado para listagem
# ------------------------------------------------------------------
class MoleculeListItem(BaseModel):
    id:            int
    nome_original: str
    nome_quimico:  Optional[str] = None
    smiles:        Optional[str] = None

    model_config = {"from_attributes": True}
