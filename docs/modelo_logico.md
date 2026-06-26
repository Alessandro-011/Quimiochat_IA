# Modelo Lógico — Sistema de Quimioinformática Inteligente

## Descrição Geral

O modelo lógico representa as entidades do sistema e seus relacionamentos em nível relacional, independente do SGBD utilizado.

---

## Diagrama Entidade-Relacionamento (Textual)

```
┌─────────────────────────────────┐
│            USERS                │
├─────────────────────────────────┤
│ PK  id            INTEGER       │
│     nome          VARCHAR(150)  │
│     email         VARCHAR(255)  │  ← UNIQUE
│     senha_hash    VARCHAR(255)  │
│     created_at    DATETIME      │
└──────────────┬──────────────────┘
               │ 1
               │
               │ N
┌──────────────▼──────────────────┐
│           SEARCHES              │
├─────────────────────────────────┤
│ PK  id              INTEGER     │
│ FK  user_id         INTEGER     │  → USERS(id)
│ FK  molecule_id     INTEGER     │  → MOLECULES(id)
│     search_time     DATETIME    │
│     response_time_ms INTEGER    │
└──────┬──────────────────┬───────┘
       │ 1                │ 1
       │                  │
       │ 1                │ 1
┌──────▼──────┐   ┌───────▼───────────────────┐
│  AI_RESULTS │   │      PUBCHEM_RESULTS       │
├─────────────┤   ├───────────────────────────┤
│ PK id  INT  │   │ PK id             INTEGER  │
│ FK search_id│   │ FK search_id      INTEGER  │ → SEARCHES(id)
│    modelo   │   │    cid            INTEGER  │
│    resultado│   │    nome           VARCHAR  │
│    tempo_res│   │    smiles         TEXT      │
└─────────────┘   │    tempo_resposta INTEGER  │
                  └───────────────────────────┘

┌─────────────────────────────────┐
│           MOLECULES             │
├─────────────────────────────────┤
│ PK  id            INTEGER       │
│     nome_original VARCHAR(255)  │
│     nome_quimico  VARCHAR(500)  │
│     smiles        TEXT          │
│     created_at    DATETIME      │
└─────────────────────────────────┘
      ↑ N (referenciada por SEARCHES.molecule_id)
```

---

## Entidades e Atributos

### 1. USERS
| Atributo    | Tipo         | Restrições        | Descrição                        |
|-------------|--------------|-------------------|----------------------------------|
| id          | INTEGER      | PK, AUTO          | Identificador único do usuário   |
| nome        | VARCHAR(150) | NOT NULL          | Nome completo                    |
| email       | VARCHAR(255) | NOT NULL, UNIQUE  | E-mail de acesso                 |
| senha_hash  | VARCHAR(255) | NOT NULL          | Hash bcrypt da senha             |
| created_at  | DATETIME     | DEFAULT NOW()     | Data de criação da conta         |

### 2. MOLECULES
| Atributo      | Tipo         | Restrições    | Descrição                              |
|---------------|--------------|---------------|----------------------------------------|
| id            | INTEGER      | PK, AUTO      | Identificador único                    |
| nome_original | VARCHAR(255) | NOT NULL      | Nome popular (ex: "Aspirina")          |
| nome_quimico  | VARCHAR(500) | NULL          | Nomenclatura IUPAC/química             |
| smiles        | TEXT         | NULL          | Representação SMILES                   |
| created_at    | DATETIME     | DEFAULT NOW() | Data de cadastro                       |

### 3. SEARCHES
| Atributo         | Tipo     | Restrições          | Descrição                       |
|------------------|----------|---------------------|---------------------------------|
| id               | INTEGER  | PK, AUTO            | Identificador único da pesquisa |
| user_id          | INTEGER  | FK → USERS(id)      | Usuário que pesquisou           |
| molecule_id      | INTEGER  | FK → MOLECULES(id)  | Molécula pesquisada             |
| search_time      | DATETIME | DEFAULT NOW()       | Momento da pesquisa             |
| response_time_ms | INTEGER  | NULL                | Tempo total em ms               |

### 4. AI_RESULTS
| Atributo      | Tipo         | Restrições          | Descrição                         |
|---------------|--------------|---------------------|-----------------------------------|
| id            | INTEGER      | PK, AUTO            | Identificador único               |
| search_id     | INTEGER      | FK → SEARCHES(id)   | Pesquisa associada                |
| modelo        | VARCHAR(100) | NOT NULL            | Modelo IA (ex: "gemma2")          |
| resultado     | TEXT         | NULL                | JSON: {nome, smiles}              |
| tempo_resposta| INTEGER      | NULL                | Tempo de resposta em ms           |

### 5. PUBCHEM_RESULTS
| Atributo      | Tipo         | Restrições          | Descrição                         |
|---------------|--------------|---------------------|-----------------------------------|
| id            | INTEGER      | PK, AUTO            | Identificador único               |
| search_id     | INTEGER      | FK → SEARCHES(id)   | Pesquisa associada                |
| cid           | INTEGER      | NULL                | PubChem Compound ID               |
| nome          | VARCHAR(500) | NULL                | Nome retornado pelo PubChem       |
| smiles        | TEXT         | NULL                | SMILES canônico                   |
| tempo_resposta| INTEGER      | NULL                | Tempo de resposta em ms           |

---

## Cardinalidade dos Relacionamentos

| Entidade A   | Relacionamento | Entidade B      | Descrição                                    |
|--------------|----------------|-----------------|----------------------------------------------|
| USERS        | 1 : N          | SEARCHES        | Um usuário realiza muitas pesquisas          |
| MOLECULES    | 1 : N          | SEARCHES        | Uma molécula aparece em muitas pesquisas     |
| SEARCHES     | 1 : 1          | AI_RESULTS      | Cada pesquisa tem um resultado de IA         |
| SEARCHES     | 1 : 1          | PUBCHEM_RESULTS | Cada pesquisa tem um resultado PubChem       |

---

## Chaves Estrangeiras

| Tabela          | Coluna      | Referência           | Ação ON DELETE |
|-----------------|-------------|----------------------|----------------|
| searches        | user_id     | users(id)            | CASCADE        |
| searches        | molecule_id | molecules(id)        | CASCADE        |
| ai_results      | search_id   | searches(id)         | CASCADE        |
| pubchem_results | search_id   | searches(id)         | CASCADE        |

---

## Índices Criados

| Tabela          | Coluna      | Tipo  | Propósito                              |
|-----------------|-------------|-------|----------------------------------------|
| users           | email       | UNIQUE| Autenticação por e-mail                |
| searches        | user_id     | INDEX | Filtro de histórico por usuário        |
| searches        | molecule_id | INDEX | Busca de pesquisas por molécula        |
| ai_results      | search_id   | INDEX | Junção com searches                    |
| pubchem_results | search_id   | INDEX | Junção com searches                    |
| molecules       | nome_original| INDEX| Busca por nome popular                 |
