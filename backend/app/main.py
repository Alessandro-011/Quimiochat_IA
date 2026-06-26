"""
main.py
Ponto de entrada da aplicação FastAPI.
TCC — Sistema de Quimioinformática Inteligente
Curso: Análise e Desenvolvimento de Sistemas
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.database.database import Base, engine
from app.models import user, molecule, search_history, ai_result, pubchem_result  # noqa: F401
from app.routes.auth      import router as auth_router
from app.routes.molecules import router as molecules_router
from app.routes.searches  import router as searches_router

logging.basicConfig(
    level   = logging.INFO,
    format  = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt = "%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Iniciando Sistema de Quimioinformática Inteligente...")
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Banco de dados inicializado.")
    yield
    logger.info("🛑 Servidor encerrado.")


app = FastAPI(
    title       = "🧪 Sistema de Quimioinformática Inteligente",
    description = (
        "API RESTful para pesquisa inteligente de moléculas químicas.\n\n"
        "**Funcionalidades:**\n"
        "- Autenticação JWT com bcrypt\n"
        "- Pesquisa via **Ollama/Gemma2** e **API PubChem** em paralelo\n"
        "- Comparação de resultados com medição de tempo\n"
        "- Histórico completo de pesquisas\n\n"
        "**TCC — Análise e Desenvolvimento de Sistemas**"
    ),
    version     = "1.0.0",
    contact     = {"name": "TCC Quimiochat IA", "email": "contato@quimiochat.com"},
    license_info = {"name": "MIT License"},
    lifespan    = lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins     = ["*"],
    allow_credentials = True,
    allow_methods     = ["*"],
    allow_headers     = ["*"],
)

app.include_router(auth_router)
app.include_router(molecules_router)
app.include_router(searches_router)


@app.get("/", tags=["Health Check"], summary="Status da API")
async def root():
    return JSONResponse(content={
        "status":  "online",
        "sistema": "Sistema de Quimioinformática Inteligente",
        "versao":  "1.0.0",
        "docs":    "/docs",
    })


@app.get("/health", tags=["Health Check"], summary="Health Check detalhado")
async def health_check():
    from app.services.ollama_service import check_ollama_health
    ollama_ok = await check_ollama_health()
    return {
        "api":    "online",
        "banco":  "online",
        "ollama": "online" if ollama_ok else "offline",
    }
