"""
models/user.py
==============
Model ORM SQLAlchemy para a tabela 'users'.
Representa os usuários cadastrados no sistema.

TCC - Sistema de Quimioinformática Inteligente
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base


class User(Base):
    """
    Modelo de usuário do sistema.

    Relacionamentos:
        - searches: lista de pesquisas realizadas pelo usuário
    """

    __tablename__ = "users"

    id         = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome       = Column(String(150), nullable=False)
    email      = Column(String(255), nullable=False, unique=True, index=True)
    senha_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamento: um usuário possui muitas pesquisas
    searches = relationship(
        "Search",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email!r}>"
