"""
models/pubchem_result.py
========================
Model ORM SQLAlchemy para a tabela 'pubchem_results'.
Armazena os resultados retornados pela API pública PubChem.

TCC - Sistema de Quimioinformática Inteligente
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class PubChemResult(Base):
    """
    Modelo de resultado PubChem.

    Campos:
        search_id     : FK para a pesquisa associada
        cid           : PubChem Compound ID (identificador único)
        nome          : Nome retornado pelo PubChem (geralmente em inglês)
        smiles        : SMILES canônico retornado pelo PubChem
        tempo_resposta: tempo de resposta em milissegundos
    """

    __tablename__ = "pubchem_results"

    id             = Column(Integer, primary_key=True, index=True, autoincrement=True)
    search_id      = Column(Integer, ForeignKey("searches.id", ondelete="CASCADE"), nullable=False, unique=True)
    cid            = Column(Integer, nullable=True)   # PubChem Compound ID
    nome           = Column(String(500), nullable=True)
    smiles         = Column(Text, nullable=True)
    tempo_resposta = Column(Integer, nullable=True)   # milissegundos

    # Relacionamento: pertence a uma pesquisa
    search = relationship("Search", back_populates="pubchem_result")

    def __repr__(self) -> str:
        return f"<PubChemResult id={self.id} cid={self.cid} nome={self.nome!r}>"
