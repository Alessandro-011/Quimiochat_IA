"""
models/molecule.py
==================
Model ORM SQLAlchemy para a tabela 'molecules'.
Armazena moléculas pesquisadas com seus dados químicos.

TCC - Sistema de Quimioinformática Inteligente
"""

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base


class Molecule(Base):
    """
    Modelo de molécula química.

    Campos:
        nome_original : Nome popular digitado pelo usuário (ex: 'Aspirina')
        nome_quimico  : Nomenclatura IUPAC ou química internacional
        smiles        : Representação molecular SMILES

    Relacionamentos:
        - searches: pesquisas que envolveram esta molécula
    """

    __tablename__ = "molecules"

    id            = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome_original = Column(String(255), nullable=False, index=True)
    nome_quimico  = Column(String(500), nullable=True)
    smiles        = Column(Text, nullable=True)
    created_at    = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamento: uma molécula aparece em muitas pesquisas
    searches = relationship(
        "Search",
        back_populates="molecule",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Molecule id={self.id} nome={self.nome_original!r}>"
