"""
routes/auth.py
==============
Rotas de autenticação: registro e login de usuários.

Endpoints:
    POST /auth/register  — Cadastro de novo usuário
    POST /auth/login     — Login e geração de JWT

TCC - Sistema de Quimioinformática Inteligente
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse, TokenResponse
from app.controllers.auth_controller import register_user, login_user

router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar novo usuário",
    description="Cria um novo usuário com senha hasheada via bcrypt.",
)
def route_register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Registra um novo usuário.

    - **nome**: Nome completo do usuário
    - **email**: Endereço de e-mail único
    - **senha**: Senha com mínimo de 6 caracteres
    """
    return register_user(user_data, db)


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Login de usuário",
    description="Autentica o usuário e retorna um token JWT Bearer.",
)
def route_login(login_data: UserLogin, db: Session = Depends(get_db)):
    """
    Realiza o login do usuário.

    - **email**: E-mail cadastrado
    - **senha**: Senha em texto puro

    Retorna um **access_token** JWT para uso nas rotas protegidas.
    """
    return login_user(login_data, db)
