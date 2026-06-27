-- ============================================================
-- MODELO FÍSICO — Sistema de Quimioinformática Inteligente
-- SGBD: SQLite 3
-- TCC — An�lise e Desenvolvimento de Sistemas
-- ============================================================

PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;       -- Write-Ahead Logging para concorrência
PRAGMA synchronous   = NORMAL;   -- Balanceia performance e segurança

-- ============================================================
-- TABELA 1: users
-- Armazena usuários cadastrados no sistema
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
    id         INTEGER      NOT NULL,
    nome       VARCHAR(150) NOT NULL,
    email      VARCHAR(255) NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    created_at DATETIME     NOT NULL DEFAULT (datetime('now', 'localtime')),

    CONSTRAINT pk_users        PRIMARY KEY (id   AUTOINCREMENT),
    CONSTRAINT uq_users_email  UNIQUE      (email)
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- ============================================================
-- TABELA 2: molecules
-- Armazena moléculas pesquisadas e seus dados químicos
-- ============================================================
CREATE TABLE IF NOT EXISTS molecules (
    id            INTEGER      NOT NULL,
    nome_original VARCHAR(255) NOT NULL,
    nome_quimico  VARCHAR(500)     NULL,
                 NULL,
    created_at    DATETIME     NOT NULL DEFAULT (datetime('now', 'localtime')),

    CONSTRAINT pk_molecules PRIMARY KEY (id AUTOINCREMENT)
);

CREATE INDEX IF NOT EXISTS idx_molecules_nome_original ON molecules(nome_original);

-- ============================================================
-- TABELA 3: searches
-- Registra cada pesquisa realizada (usuário + molécula)
-- ============================================================
CREATE TABLE IF NOT EXISTS searches (
    id               INTEGER  NOT NULL,
    user_id          INTEGER  NOT NULL,
    molecule_id      INTEGER  NOT NULL,
    search_time      DATETIME NOT NULL DEFAULT (datetime('now', 'localtime')),
    response_time_ms INTEGER      NULL,

    CONSTRAINT pk_searches         PRIMARY KEY (id AUTOINCREMENT),
    CONSTRAINT fk_searches_user    FOREIGN KEY (user_id)     REFERENCES users(id)     ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_searches_molecule FOREIGN KEY (molecule_id) REFERENCES molecules(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_searches_user_id     ON searches(user_id);
CREATE INDEX IF NOT EXISTS idx_searches_molecule_id ON searches(molecule_id);
CREATE INDEX IF NOT EXISTS idx_searches_time        ON searches(search_time DESC);

-- ============================================================
-- TABELA 4: ai_results
-- Resultados retornados pelo modelo de IA (Ollama/Gemma2)
-- ============================================================
CREATE TABLE IF NOT EXISTS ai_results (
    id             INTEGER      NOT NULL,
    search_id      INTEGER      NOT NULL,
    modelo         VARCHAR(100) NOT NULL DEFAULT 'gemma2',
    resultado      TEXT             NULL,  -- JSON: {"nome":"...","smiles":"..."}
    tempo_resposta INTEGER          NULL,  -- milissegundos

    CONSTRAINT pk_ai_results        PRIMARY KEY (id AUTOINCREMENT),
    CONSTRAINT fk_ai_results_search FOREIGN KEY (search_id) REFERENCES searches(id) ON DELETE CASCADE,
    CONSTRAINT uq_ai_results_search UNIQUE (search_id)       -- 1:1 com searches
);

CREATE INDEX IF NOT EXISTS idx_ai_results_search_id ON ai_results(search_id);

-- ============================================================
-- TABELA 5: pubchem_results
-- Resultados retornados pela API pública PubChem
-- ============================================================
CREATE TABLE IF NOT EXISTS pubchem_results (
    id             INTEGER      NOT NULL,
    search_id      INTEGER      NOT NULL,
    cid            INTEGER          NULL,  -- PubChem Compound ID
    nome           VARCHAR(500)     NULL,
    smiles         TEXT             NULL,
    tempo_resposta INTEGER          NULL,  -- milissegundos

    CONSTRAINT pk_pubchem_results        PRIMARY KEY (id AUTOINCREMENT),
    CONSTRAINT fk_pubchem_results_search FOREIGN KEY (search_id) REFERENCES searches(id) ON DELETE CASCADE,
    CONSTRAINT uq_pubchem_results_search UNIQUE (search_id)       -- 1:1 com searches
);

CREATE INDEX IF NOT EXISTS idx_pubchem_results_search_id ON pubchem_results(search_id);
CREATE INDEX IF NOT EXISTS idx_pubchem_results_cid       ON pubchem_results(cid);

-- ============================================================
-- VIEWS úteis para relatórios acadêmicos
-- ============================================================

-- View: Histórico completo de pesquisas com todos os dados
CREATE VIEW IF NOT EXISTS vw_historico_completo AS
SELECT
    s.id                        AS search_id,
    u.nome                      AS usuario,
    u.email                     AS email_usuario,
    m.nome_original             AS molecula_pesquisada,
    m.nome_quimico              AS nome_quimico,
    m.smiles                    AS smiles_banco,
    s.search_time               AS data_pesquisa,
    s.response_time_ms          AS tempo_total_ms,
    ai.modelo                   AS modelo_ia,
    ai.resultado                AS resultado_ia_json,
    ai.tempo_resposta           AS tempo_ia_ms,
    pc.cid                      AS pubchem_cid,
    pc.nome                     AS pubchem_nome,
    pc.smiles                   AS pubchem_smiles,
    pc.tempo_resposta           AS tempo_pubchem_ms
FROM searches s
JOIN users             u  ON s.user_id     = u.id
JOIN molecules         m  ON s.molecule_id = m.id
LEFT JOIN ai_results   ai ON s.id          = ai.search_id
LEFT JOIN pubchem_results pc ON s.id       = pc.search_id
ORDER BY s.search_time DESC;

-- View: Estatísticas por molécula
CREATE VIEW IF NOT EXISTS vw_estatisticas_moleculas AS
SELECT
    m.nome_original,
    COUNT(s.id)              AS total_pesquisas,
    AVG(s.response_time_ms)  AS tempo_medio_ms,
    MIN(s.response_time_ms)  AS tempo_minimo_ms,
    MAX(s.response_time_ms)  AS tempo_maximo_ms,
    AVG(ai.tempo_resposta)   AS tempo_medio_ia_ms,
    AVG(pc.tempo_resposta)   AS tempo_medio_pubchem_ms
FROM molecules m
LEFT JOIN searches         s  ON m.id = s.molecule_id
LEFT JOIN ai_results       ai ON s.id = ai.search_id
LEFT JOIN pubchem_results  pc ON s.id = pc.search_id
GROUP BY m.id, m.nome_original
ORDER BY total_pesquisas DESC;
