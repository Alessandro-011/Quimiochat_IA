"""
models/ai_result.py
===================
Model ORM SQLAlchemy para a tabela 'ai_results'.
Armazena os resultados retornados pelo modelo de IA (Ollama/Gemma2).

TCC - Sistema de Quimioinformática Inteligente
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class AIResult(Base):
    """
    Modelo de resultado de IA.

    Campos:
        search_id     : FK para a pesquisa associada
        modelo        : nome do modelo usado (ex: 'gemma2')
        resultado     : JSON string com nome e SMILES retornados
        tempo_resposta: tempo de resposta em milissegundos
    """

    __tablename__ = "ai_results"

    id             = Column(Integer, primary_key=True, index=True, autoincrement=True)
    search_id      = Column(Integer, ForeignKey("searches.id", ondelete="CASCADE"), nullable=False, unique=True)
    modelo         = Column(String(100), nullable=False, default="gemma2")
    resultado      = Column(Text, nullable=True)   # JSON: {"nome": "...", "smiles": "..."}
    tempo_resposta = Column(Integer, nullable=True) # milissegundos

    # Relacionamento: pertence a uma pesquisa
    search = relationship("Search", back_populates="ai_result")

    def __repr__(self) -> str:
        return f"<AIResult id={self.id} search_id={self.search_id} modelo={self.modelo!r}>"
