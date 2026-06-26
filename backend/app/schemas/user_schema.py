"""
schemas/user_schema.py
======================
Schemas Pydantic para validação e serialização de dados de usuários.

TCC - Sistema de Quimioinformática Inteligente
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator


# ------------------------------------------------------------------
# Schema base — campos compartilhados
# ------------------------------------------------------------------
class UserBase(BaseModel):
    nome:  str   = Field(..., min_length=2,  max_length=150, examples=["João Silva"])
    email: EmailStr = Field(..., examples=["joao@exemplo.com"])


# ------------------------------------------------------------------
# Schema de criação — inclui senha em texto puro (apenas na entrada)
# ------------------------------------------------------------------
class UserCreate(UserBase):
    senha: str = Field(..., min_length=6, max_length=100, examples=["senha123"])

    @field_validator("nome")
    @classmethod
    def nome_nao_vazio(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("O nome não pode ser vazio.")
        return v.strip()


# ------------------------------------------------------------------
# Schema de atualização — todos os campos opcionais
# ------------------------------------------------------------------
class UserUpdate(BaseModel):
    nome:  Optional[str]      = Field(None, min_length=2, max_length=150)
    email: Optional[EmailStr] = None
    senha: Optional[str]      = Field(None, min_length=6)


# ------------------------------------------------------------------
# Schema de resposta — NUNCA retorna senha ou hash
# ------------------------------------------------------------------
class UserResponse(UserBase):
    id:         int
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ------------------------------------------------------------------
# Schema de login
# ------------------------------------------------------------------
class UserLogin(BaseModel):
    email: EmailStr = Field(..., examples=["joao@exemplo.com"])
    senha: str      = Field(..., min_length=1, examples=["senha123"])


# ------------------------------------------------------------------
# Schema do token JWT retornado no login
# ------------------------------------------------------------------
class TokenResponse(BaseModel):
    access_token: str
    token_type:   str = "bearer"
    user:         UserResponse
