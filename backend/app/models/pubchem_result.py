"""
models/pubchem_result.py
========================
Model ORM SQLAlchemy para a tabela 'pubchem_results'.
Armazena os resultados científicos retornados pela API pública PubChem.

TCC - Análise e Desenvolvimento de Sistemas
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
        nome_comum       : Nome popular retornado pelo PubChem (Title)
        nome_iupac       : Nome químico oficial (IUPACName)
        smiles_canonico  : Representação SMILES canônica
        smiles_isomerico : Representação SMILES isomérica
        formula          : Fórmula molecular
        massa            : Massa molecular
        tempo_resposta   : Tempo de resposta em milissegundos
    """

    __tablename__ = "pubchem_results"

    id               = Column(Integer, primary_key=True, index=True, autoincrement=True)
    search_id        = Column(Integer, ForeignKey("searches.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    cid              = Column(Integer, nullable=True)
    nome_comum       = Column(String(500), nullable=True)
    nome_iupac       = Column(String(1000), nullable=True)
    smiles_canonico  = Column(Text, nullable=True)
    smiles_isomerico = Column(Text, nullable=True)
    formula          = Column(String(100), nullable=True)
    massa            = Column(String(50), nullable=True)
    
    tempo_resposta   = Column(Integer, nullable=True)

    # Relacionamento: pertence a uma pesquisa
    search = relationship("Search", back_populates="pubchem_result")

    def __repr__(self) -> str:
        return f"<PubChemResult id={self.id} cid={self.cid} nome_comum={self.nome_comum!r}>"
