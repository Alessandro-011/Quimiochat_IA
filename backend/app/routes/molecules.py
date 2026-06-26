"""
routes/molecules.py
===================
Rotas para gerenciamento de moléculas (protegidas por JWT).

Endpoints:
    GET  /molecules         — Lista todas as moléculas
    GET  /molecules/{id}    — Busca molécula por ID
    POST /molecules/search  — Pesquisa molécula via IA + PubChem (regra principal do TCC)
    POST /molecules         — Cria molécula manualmente
    DELETE /molecules/{id}  — Remove molécula

TCC - Sistema de Quimioinformática Inteligente
"""

from typing import List

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.middleware.jwt_auth import get_current_user
from app.models.user import User
from app.schemas.molecule_schema import MoleculeCreate, MoleculeResponse, MoleculeListItem
from app.schemas.search_schema import SearchRequest, SearchResponse
from app.controllers.molecule_controller import (
    list_molecules,
    get_molecule_by_id,
    create_molecule,
    delete_molecule,
)
from app.controllers.search_controller import search_molecule

router = APIRouter(
    prefix="/molecules",
    tags=["Moléculas"],
)


@router.get(
    "",
    response_model=List[MoleculeListItem],
    summary="Listar moléculas",
    description="Retorna todas as moléculas cadastradas no banco.",
)
def route_list_molecules(
    skip:  int = Query(0,  ge=0),
    limit: int = Query(50, ge=1, le=200),
    db:    Session = Depends(get_db),
    _:     User    = Depends(get_current_user),
):
    """Lista todas as moléculas com paginação (skip/limit)."""
    return list_molecules(db, skip=skip, limit=limit)


@router.get(
    "/{molecule_id}",
    response_model=MoleculeResponse,
    summary="Buscar molécula por ID",
)
def route_get_molecule(
    molecule_id: int,
    db: Session = Depends(get_db),
    _:  User    = Depends(get_current_user),
):
    """Retorna os dados completos de uma molécula pelo seu ID."""
    return get_molecule_by_id(molecule_id, db)


@router.post(
    "/search",
    response_model=SearchResponse,
    status_code=status.HTTP_200_OK,
    summary="Pesquisar molécula (IA + PubChem)",
    description=(
        "Rota principal do TCC. Recebe um nome popular, consulta o Ollama/Gemma2 e "
        "a API PubChem em paralelo, salva os resultados no banco e retorna o JSON comparativo."
    ),
)
async def route_search_molecule(
    request:      SearchRequest,
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user),
):
    """
    **Pesquisa inteligente de molécula.**

    - Envia o nome para o **Ollama (Gemma2)** para tradução química e geração de SMILES.
    - Consulta a **API PubChem** em paralelo.
    - Mede o **tempo de resposta** de cada fonte.
    - Salva tudo no banco de dados.
    - Retorna um JSON comparativo com os dados de ambas as fontes.
    """
    return await search_molecule(request, current_user, db)


@router.post(
    "",
    response_model=MoleculeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar molécula manualmente",
)
def route_create_molecule(
    molecule_data: MoleculeCreate,
    db: Session = Depends(get_db),
    _:  User    = Depends(get_current_user),
):
    """Cria uma nova entrada de molécula manualmente (sem pesquisa por IA)."""
    return create_molecule(molecule_data, db)


@router.delete(
    "/{molecule_id}",
    status_code=status.HTTP_200_OK,
    summary="Remover molécula",
)
def route_delete_molecule(
    molecule_id: int,
    db: Session = Depends(get_db),
    _:  User    = Depends(get_current_user),
):
    """Remove uma molécula pelo ID."""
    return delete_molecule(molecule_id, db)
