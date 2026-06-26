"""
models/search_history.py
========================
Model ORM SQLAlchemy para a tabela 'searches'.
Registra cada pesquisa realizada (usuário + molécula + tempo).

TCC - Sistema de Quimioinformática Inteligente
"""

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base


class Search(Base):
    """
    Modelo de registro de pesquisa.

    Relacionamentos:
        - user       : usuário que realizou a pesquisa
        - molecule   : molécula pesquisada
        - ai_result  : resultado retornado pela IA (Ollama)
        - pubchem_result : resultado retornado pela PubChem API
    """

    __tablename__ = "searches"

    id               = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id          = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    molecule_id      = Column(Integer, ForeignKey("molecules.id", ondelete="CASCADE"), nullable=False)
    search_time      = Column(DateTime(timezone=True), server_default=func.now())
    response_time_ms = Column(Integer, nullable=True)  # Tempo total da pesquisa completa

    # Relacionamentos
    user     = relationship("User",     back_populates="searches")
    molecule = relationship("Molecule", back_populates="searches")

    ai_result     = relationship(
        "AIResult",
        back_populates="search",
        uselist=False,
        cascade="all, delete-orphan",
    )
    pubchem_result = relationship(
        "PubChemResult",
        back_populates="search",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Search id={self.id} user_id={self.user_id} molecule_id={self.molecule_id}>"
