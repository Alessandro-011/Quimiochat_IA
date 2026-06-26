"""
controllers/molecule_controller.py
===================================
Lógica de negócio para CRUD de moléculas.

TCC - Sistema de Quimioinformática Inteligente
"""

import logging
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.molecule import Molecule
from app.schemas.molecule_schema import MoleculeCreate, MoleculeResponse, MoleculeListItem

logger = logging.getLogger(__name__)


def list_molecules(db: Session, skip: int = 0, limit: int = 50) -> List[MoleculeListItem]:
    """
    Lista todas as moléculas cadastradas no banco com paginação.

    Args:
        db   : Sessão do banco.
        skip : Offset para paginação.
        limit: Máximo de registros retornados.

    Returns:
        Lista de MoleculeListItem.
    """
    molecules = db.query(Molecule).offset(skip).limit(limit).all()
    return [MoleculeListItem.model_validate(m) for m in molecules]


def get_molecule_by_id(molecule_id: int, db: Session) -> MoleculeResponse:
    """
    Busca uma molécula pelo ID.

    Args:
        molecule_id: ID da molécula.
        db         : Sessão do banco.

    Returns:
        MoleculeResponse com os dados da molécula.

    Raises:
        HTTPException 404: Se a molécula não existir.
    """
    molecule = db.query(Molecule).filter(Molecule.id == molecule_id).first()
    if not molecule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Molécula com ID {molecule_id} não encontrada.",
        )
    return MoleculeResponse.model_validate(molecule)


def create_molecule(molecule_data: MoleculeCreate, db: Session) -> MoleculeResponse:
    """
    Cria uma nova molécula manualmente (sem pesquisa por IA).

    Args:
        molecule_data: Dados da molécula.
        db           : Sessão do banco.

    Returns:
        MoleculeResponse com a molécula criada.

    Raises:
        HTTPException 409: Se já existir molécula com mesmo nome original.
    """
    existing = (
        db.query(Molecule)
        .filter(Molecule.nome_original.ilike(molecule_data.nome_original))
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe uma molécula com este nome original.",
        )

    molecule = Molecule(
        nome_original = molecule_data.nome_original,
        nome_quimico  = molecule_data.nome_quimico,
        smiles        = molecule_data.smiles,
    )
    db.add(molecule)
    db.commit()
    db.refresh(molecule)
    return MoleculeResponse.model_validate(molecule)


def delete_molecule(molecule_id: int, db: Session) -> dict:
    """
    Remove uma molécula pelo ID.

    Args:
        molecule_id: ID da molécula a excluir.
        db         : Sessão do banco.

    Returns:
        Mensagem de confirmação.

    Raises:
        HTTPException 404: Se a molécula não existir.
    """
    molecule = db.query(Molecule).filter(Molecule.id == molecule_id).first()
    if not molecule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Molécula com ID {molecule_id} não encontrada.",
        )
    db.delete(molecule)
    db.commit()
    logger.info("Molécula removida: id=%d nome=%s", molecule_id, molecule.nome_original)
    return {"message": f"Molécula '{molecule.nome_original}' removida com sucesso."}
