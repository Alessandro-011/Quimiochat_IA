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
        search_id        : FK para a pesquisa associada
        cid              : PubChem Compound ID (identificador único)
        nome_comum       : Nome preferencial retornado pelo PubChem
        nome_iupac       : Nome IUPAC oficial da molécula
        smiles_canonico  : Canonical SMILES (oficial principal)
        smiles_isomerico : Isomeric SMILES (usado como fallback visual)
        formula          : Fórmula molecular
        massa            : Massa molecular
        tempo_resposta   : tempo de resposta em milissegundos
    """

    __tablename__ = "pubchem_results"

    id               = Column(Integer, primary_key=True, index=True, autoincrement=True)
    search_id        = Column(Integer, ForeignKey("searches.id", ondelete="CASCADE"), nullable=False, unique=True)
    cid              = Column(Integer, nullable=True)
    nome_comum       = Column(String(500), nullable=True)
    nome_iupac       = Column(String(500), nullable=True)
    smiles_canonico  = Column(Text, nullable=True)
    smiles_isomerico = Column(Text, nullable=True)
    formula          = Column(String(100), nullable=True)
    massa            = Column(String(100), nullable=True)
    tempo_resposta   = Column(Integer, nullable=True)

    # Relacionamento: pertence a uma pesquisa
    search = relationship("Search", back_populates="pubchem_result")

    def __repr__(self) -> str:
        return f"<PubChemResult id={self.id} cid={self.cid} comum={self.nome_comum!r}>"
