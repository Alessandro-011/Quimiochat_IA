-- ============================================================
-- Sistema de Quimioinformática Inteligente
-- Script de Inserção de Dados de Teste
-- TCC - An�lise e Desenvolvimento de Sistemas
-- ============================================================

PRAGMA foreign_keys = ON;

-- ------------------------------------------------------------
-- Dados de Teste: users
-- Senhas: admin123 e user123 (hashes bcrypt gerados externamente)
-- ------------------------------------------------------------
INSERT OR IGNORE INTO users (nome, email, senha_hash) VALUES
    ('Admin Sistema',  'admin@quimiochat.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW'),
    ('João Pesquisador', 'joao@quimiochat.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW'),
    ('Maria Química',   'maria@quimiochat.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW');

-- ------------------------------------------------------------
-- Dados de Teste: molecules
-- ------------------------------------------------------------
INSERT OR IGNORE INTO molecules (nome_original, nome_quimico, smiles) VALUES
    ('Aspirina',   'Ácido acetilsalicílico', 'CC(=O)Oc1ccccc1C(=O)O'),
    ('Cafeína',    '1,3,7-trimetilxantina',  'Cn1c(=O)c2c(ncn2C)n(c1=O)C'),
    ('Glicose',    'D-Glicose',              'OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O'),
    ('Paracetamol','Acetaminofeno',           'CC(=O)Nc1ccc(O)cc1'),
    ('Etanol',     'Álcool etílico',          'CCO'),
    ('Dopamina',   '4-(2-aminoetil)benzeno-1,2-diol', 'NCCc1ccc(O)c(O)c1'),
    ('Serotonina', '3-(2-aminoetil)-1H-indol-5-ol',   'NCCc1c[nH]c2ccc(O)cc12'),
    ('Ibuprofeno', 'Ácido (RS)-2-(4-(2-metilpropil)fenil)propanoico', 'CC(C)Cc1ccc(cc1)[C@@H](C)C(=O)O');

-- ------------------------------------------------------------
-- Dados de Teste: searches
-- ------------------------------------------------------------
INSERT OR IGNORE INTO searches (user_id, molecule_id, response_time_ms) VALUES
    (1, 1, 1250),
    (1, 2, 980),
    (2, 3, 1540),
    (2, 4, 870),
    (3, 1, 1100),
    (3, 5, 650);

-- ------------------------------------------------------------
-- Dados de Teste: ai_results
-- ------------------------------------------------------------
INSERT OR IGNORE INTO ai_results (search_id, modelo, resultado, tempo_resposta) VALUES
    (1, 'gemma2', '{"nome":"Ácido acetilsalicílico","smiles":"CC(=O)Oc1ccccc1C(=O)O"}', 1100),
    (2, 'gemma2', '{"nome":"1,3,7-trimetilxantina","smiles":"Cn1c(=O)c2c(ncn2C)n(c1=O)C"}', 820),
    (3, 'gemma2', '{"nome":"D-Glicose","smiles":"OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O"}', 1400),
    (4, 'gemma2', '{"nome":"Acetaminofeno","smiles":"CC(=O)Nc1ccc(O)cc1"}', 750),
    (5, 'gemma2', '{"nome":"Ácido acetilsalicílico","smiles":"CC(=O)Oc1ccccc1C(=O)O"}', 950),
    (6, 'gemma2', '{"nome":"Álcool etílico","smiles":"CCO"}', 580);

-- ------------------------------------------------------------
-- Dados de Teste: pubchem_results
-- ------------------------------------------------------------
INSERT OR IGNORE INTO pubchem_results (search_id, cid, nome, smiles, tempo_resposta) VALUES
    (1, 2244,  'Aspirin',         'CC(=O)Oc1ccccc1C(=O)O',                         150),
    (2, 2519,  'Caffeine',        'Cn1c(=O)c2c(ncn2C)n(c1=O)C',                    120),
    (3, 5793,  'Glucose',         'OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O',        140),
    (4, 1983,  'Acetaminophen',   'CC(=O)Nc1ccc(O)cc1',                             130),
    (5, 2244,  'Aspirin',         'CC(=O)Oc1ccccc1C(=O)O',                         155),
    (6, 702,   'Ethanol',         'CCO',                                             110);
