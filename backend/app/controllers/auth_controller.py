"""
controllers/auth_controller.py
==============================
Lógica de negócio para autenticação: registro e login de usuários.

TCC - Sistema de Quimioinformática Inteligente
"""

import logging
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse, TokenResponse
from app.utils.security import hash_password, verify_password, create_access_token

logger = logging.getLogger(__name__)


def register_user(user_data: UserCreate, db: Session) -> UserResponse:
    """
    Registra um novo usuário no sistema.

    Validações:
        - Email deve ser único.
        - Senha é hashada com bcrypt antes de salvar.

    Args:
        user_data: Dados do usuário (nome, email, senha).
        db       : Sessão do banco.

    Returns:
        UserResponse com os dados do usuário criado (sem senha).

    Raises:
        HTTPException 409: Se o email já estiver cadastrado.
    """
    # Verifica se email já existe
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este e-mail já está cadastrado.",
        )

    # Cria o usuário com senha hasheada
    new_user = User(
        nome       = user_data.nome,
        email      = user_data.email,
        senha_hash = hash_password(user_data.senha),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logger.info("Novo usuário registrado: %s", new_user.email)
    return UserResponse.model_validate(new_user)


def login_user(login_data: UserLogin, db: Session) -> TokenResponse:
    """
    Autentica um usuário e retorna um JWT.

    Validações:
        - Email deve existir.
        - Senha deve corresponder ao hash armazenado.

    Args:
        login_data: Email e senha em texto puro.
        db        : Sessão do banco.

    Returns:
        TokenResponse com access_token JWT e dados do usuário.

    Raises:
        HTTPException 401: Se as credenciais forem inválidas.
    """
    user = db.query(User).filter(User.email == login_data.email).first()

    if not user or not verify_password(login_data.senha, user.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Gera o JWT com o email como subject
    token = create_access_token(data={"sub": user.email})

    logger.info("Login bem-sucedido: %s", user.email)
    return TokenResponse(
        access_token = token,
        token_type   = "bearer",
        user         = UserResponse.model_validate(user),
    )
