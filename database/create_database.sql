-- ============================================================
-- Sistema de Quimioinformática Inteligente
-- Script de Criação do Banco de Dados SQLite
-- TCC - An�lise e Desenvolvimento de Sistemas
-- ============================================================

PRAGMA foreign_keys = ON;

-- ------------------------------------------------------------
-- Tabela 1: users
-- Armazena os usuários do sistema
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nome        TEXT    NOT NULL,
    email       TEXT    NOT NULL UNIQUE,
    senha_hash  TEXT    NOT NULL,
    created_at  DATETIME DEFAULT (datetime('now', 'localtime'))
);

-- ------------------------------------------------------------
-- Tabela 2: molecules
-- Armazena as moléculas pesquisadas e seus dados químicos
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS molecules (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_original TEXT    NOT NULL,
    nome_quimico  TEXT,
    smiles        TEXT,
    created_at    DATETIME DEFAULT (datetime('now', 'localtime'))
);

-- ------------------------------------------------------------
-- Tabela 3: searches
-- Registra cada pesquisa realizada por um usuário
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS searches (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL,
    molecule_id     INTEGER NOT NULL,
    search_time     DATETIME DEFAULT (datetime('now', 'localtime')),
    response_time_ms INTEGER,
    FOREIGN KEY (user_id)     REFERENCES users(id)     ON DELETE CASCADE,
    FOREIGN KEY (molecule_id) REFERENCES molecules(id) ON DELETE CASCADE
);

-- ------------------------------------------------------------
-- Tabela 4: ai_results
-- Armazena os resultados retornados pelo modelo de IA (Ollama)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS ai_results (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    search_id       INTEGER NOT NULL,
    modelo          TEXT    NOT NULL DEFAULT 'gemma2',
    resultado       TEXT,
    tempo_resposta  INTEGER,
    FOREIGN KEY (search_id) REFERENCES searches(id) ON DELETE CASCADE
);

-- ------------------------------------------------------------
-- Tabela 5: pubchem_results
-- Armazena os resultados retornados pela API PubChem
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS pubchem_results (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    search_id       INTEGER NOT NULL,
    cid             INTEGER,
    nome            TEXT,
    smiles          TEXT,
    tempo_resposta  INTEGER,
    FOREIGN KEY (search_id) REFERENCES searches(id) ON DELETE CASCADE
);

-- ------------------------------------------------------------
-- Índices para otimização de consultas
-- ------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_searches_user_id     ON searches(user_id);
CREATE INDEX IF NOT EXISTS idx_searches_molecule_id ON searches(molecule_id);
CREATE INDEX IF NOT EXISTS idx_ai_results_search_id ON ai_results(search_id);
CREATE INDEX IF NOT EXISTS idx_pubchem_search_id    ON pubchem_results(search_id);
CREATE INDEX IF NOT EXISTS idx_molecules_nome       ON molecules(nome_original);
