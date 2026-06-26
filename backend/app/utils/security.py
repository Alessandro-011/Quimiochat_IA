"""
utils/security.py
Hash de senha via bcrypt e geração/validação de JWT.

Usa bcrypt diretamente (sem passlib) — compatível com Python 3.14+ e bcrypt 5.x.
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
import jwt
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY                  = os.getenv("SECRET_KEY", "TROQUE_ESTA_CHAVE_EM_PRODUCAO_12345")
ALGORITHM                   = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


def hash_password(senha: str) -> str:
    senha_bytes = senha.encode("utf-8")
    salt        = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(senha_bytes, salt).decode("utf-8")


def verify_password(senha_pura: str, senha_hash: str) -> bool:
    try:
        return bcrypt.checkpw(
            senha_pura.encode("utf-8"),
            senha_hash.encode("utf-8"),
        )
    except Exception:
        return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
