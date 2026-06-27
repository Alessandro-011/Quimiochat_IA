# 🧪 Sistema de Quimioinformática Inteligente

> **TCC — Trabalho de Conclusão de Curso | Análise e Desenvolvimento de Sistemas**  
> Integração entre pesquisa química tradicional e Inteligência Artificial Generativa

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?logo=fastapi)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?logo=streamlit)](https://streamlit.io)
[![Ollama](https://img.shields.io/badge/Ollama-Gemma2-orange)](https://ollama.com)
[![SQLite](https://img.shields.io/badge/SQLite-3-lightblue?logo=sqlite)](https://sqlite.org)

---

## 📦 Nota de Entrega (Atividade 2)

**Prezado Professor**

Este projeto foi zipado e está sendo entregue de forma **completa e integrada**, contendo todos os requisitos exigidos para a **Atividade 2**, estruturados nas seguintes pastas para facilitar a sua avaliação:

* **[Item 2.1] Modelagem do Banco de Dados:** Os modelos Conceitual (`DER.png`), Lógico (`modelo_logico.md`) e Físico com scripts de Inserção de Dados de Teste (`modelo_fisico.sql`) estão todos na pasta `docs/`.
* **[Item 2.2] Documentação da API:** O descritivo completo das rotas, parâmetros e exemplos de JSON encontra-se no arquivo `API_DOCUMENTATION.md` (na pasta `docs/`). O Swagger Interativo também está configurado na rota `/docs`.
* **[Item 2.3] Backend Implementado:** O código-fonte completo (com controllers, models, schemas e rotas) está na pasta `backend/`. O CRUD e as regras de negócio foram implementadas em FastAPI.
* **[Item 2.4] Integração com o Frontend:** O sistema já se encontra totalmente integrado ao frontend desenvolvido na Atividade 1. O código da interface está na pasta `frontend/`.
* **[Item 2.5] Instruções e README:** Este próprio documento atende aos requisitos de documentação de ambiente, dependências e inicialização do projeto.

---

## 📋 Descrição

O **Sistema de Quimioinformática Inteligente** é uma aplicação web que permite pesquisar moléculas químicas usando nomes populares em português. O sistema integra:

- **IA Generativa Local** (Ollama/Gemma2) para tradução semântica e geração de SMILES
- **API PubChem** (banco de dados químico oficial da NCBI) para consulta de dados validados
- **Comparativo em tempo real** entre as fontes, com medição de tempo de resposta
- **Autenticação segura** com JWT e bcrypt
- **Histórico completo** de todas as pesquisas realizadas

### Fluxo Principal

```
Usuário digita "Aspirina"
         ↓
   [Backend FastAPI]
    ↙           ↘
[Ollama/Gemma2] [PubChem API]  ← Consultas paralelas (asyncio)
    ↘           ↙
   Comparação de resultados
         ↓
   Salva no SQLite
         ↓
   Retorna JSON comparativo
         ↓
   [Frontend Streamlit]
   Exibe estrutura 2D + métricas
```

---

## 🏗️ Arquitetura

### Padrão MVC (Model-View-Controller)

```
TCC_Quimiochat_IA/
│
├── backend/                        # API REST (FastAPI)
│   ├── app/
│   │   ├── main.py                 # Ponto de entrada da aplicação
│   │   ├── database/
│   │   │   └── database.py         # Configuração SQLAlchemy + SQLite
│   │   ├── models/                 # [M] Camada de dados (ORM)
│   │   │   ├── user.py
│   │   │   ├── molecule.py
│   │   │   ├── search_history.py
│   │   │   ├── ai_result.py
│   │   │   └── pubchem_result.py
│   │   ├── schemas/                # Validação Pydantic (DTOs)
│   │   │   ├── user_schema.py
│   │   │   ├── molecule_schema.py
│   │   │   └── search_schema.py
│   │   ├── routes/                 # Definição das rotas HTTP
│   │   │   ├── auth.py
│   │   │   ├── molecules.py
│   │   │   └── searches.py
│   │   ├── controllers/            # [C] Lógica de negócio
│   │   │   ├── auth_controller.py
│   │   │   ├── molecule_controller.py
│   │   │   └── search_controller.py
│   │   ├── services/               # Integração com APIs externas
│   │   │   ├── ollama_service.py   # Gemma2 via Ollama
│   │   │   ├── pubchem_service.py  # API PubChem
│   │   │   └── molecule_service.py # Orquestrador paralelo
│   │   ├── middleware/
│   │   │   └── jwt_auth.py         # Validação JWT
│   │   └── utils/
│   │       └── security.py         # bcrypt + JWT
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/                       # [V] Interface gráfica
│   └── streamlit_app.py            # Frontend Streamlit
│
├── database/                       # Scripts SQL
│   ├── create_database.sql
│   └── insert_test_data.sql
│
├── docs/                           # Documentação acadêmica
│   ├── modelo_logico.md
│   ├── modelo_fisico.sql
│   └── API_DOCUMENTATION.md
│
└── README.md
```

### Stack Tecnológica

| Camada       | Tecnologia          | Propósito                               |
|--------------|---------------------|-----------------------------------------|
| Backend      | Python 3.11+        | Linguagem principal                     |
| Framework    | FastAPI 0.115       | API REST + Swagger automático           |
| ORM          | SQLAlchemy 2.0      | Mapeamento objeto-relacional            |
| Validação    | Pydantic 2.x        | Schemas e validação de dados            |
| Banco        | SQLite 3            | Armazenamento relacional                |
| Autenticação | PyJWT + bcrypt      | Segurança JWT + hash de senhas          |
| HTTP Client  | httpx               | Requisições assíncronas (PubChem+Ollama)|
| IA Local     | Ollama + Gemma2     | Tradução química e geração SMILES       |
| Frontend     | Streamlit           | Interface web interativa                |

---

## 🚀 Instalação e Execução

### Pré-requisitos

- [Python 3.11+](https://python.org/downloads/)
- [Ollama](https://ollama.com/download) instalado e configurado
- Conexão com a internet (para API PubChem)

### 1. Clonar o projeto

```bash
git clone <url-do-repositorio>
cd TCC_Quimiochat_IA
```

### 2. Configurar o Ollama

```bash
# Instalar o Ollama (siga as instruções em https://ollama.com)
# Depois, baixar o modelo Gemma2:
ollama pull gemma2

# Iniciar o Ollama (deve ficar rodando em background):
ollama serve
```

### 3. Configurar o Backend

```bash
cd backend

# Criar ambiente virtual Python
python -m venv venv

# Ativar o ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
copy .env.example .env
# Edite o arquivo .env com suas configurações
```

### 4. Iniciar o Backend (FastAPI)

```bash
# Dentro da pasta backend/ com o venv ativado:
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

O servidor iniciará em: `http://localhost:8000`  
Swagger UI: `http://localhost:8000/docs`

### 5. Iniciar o Frontend (Streamlit)

Em um **novo terminal**:

```bash
cd frontend

# Com o venv ativado:
pip install streamlit requests

streamlit run streamlit_app.py
```

O frontend abrirá em: `http://localhost:8501`

---

## 🔧 Variáveis de Ambiente

Crie o arquivo `backend/.env` baseado em `backend/.env.example`:

```env
# Banco de dados
DATABASE_URL=sqlite:///./quimiochat.db

# JWT — ALTERE ESTA CHAVE EM PRODUÇÃO!
SECRET_KEY=sua-chave-secreta-aleatoria-longa
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=gemma2
OLLAMA_TIMEOUT=120
```

> ⚠️ **Nunca commite o arquivo `.env` no controle de versão!**

---

## 📡 Endpoints da API

### Autenticação
| Método | Endpoint         | Descrição              | Auth |
|--------|-----------------|------------------------|------|
| POST   | `/auth/register` | Registrar usuário      | ❌   |
| POST   | `/auth/login`    | Login → retorna JWT    | ❌   |

### Moléculas
| Método | Endpoint                | Descrição                        | Auth |
|--------|------------------------|----------------------------------|------|
| GET    | `/molecules`            | Listar moléculas                 | ✅   |
| GET    | `/molecules/{id}`       | Buscar por ID                    | ✅   |
| POST   | `/molecules/search`     | **Pesquisa IA + PubChem** ⭐     | ✅   |
| POST   | `/molecules`            | Criar manualmente                | ✅   |
| DELETE | `/molecules/{id}`       | Remover                          | ✅   |

### Histórico
| Método | Endpoint          | Descrição                    | Auth |
|--------|------------------|------------------------------|------|
| GET    | `/search/history` | Histórico do usuário logado | ✅   |

Documentação completa em: [`docs/API_DOCUMENTATION.md`](docs/API_DOCUMENTATION.md)

---

## 🗃️ Banco de Dados

### Tabelas

| Tabela           | Descrição                                     |
|------------------|-----------------------------------------------|
| `users`          | Usuários do sistema                           |
| `molecules`      | Moléculas pesquisadas com dados químicos      |
| `searches`       | Registro de cada pesquisa (usuário + molécula)|
| `ai_results`     | Resultados do Ollama/Gemma2                   |
| `pubchem_results`| Resultados da API PubChem                     |

### Dados de Teste

O arquivo `database/insert_test_data.sql` insere dados de teste. Para cargá-los manualmente:

```bash
# Com sqlite3 instalado:
sqlite3 backend/quimiochat.db < database/create_database.sql
sqlite3 backend/quimiochat.db < database/insert_test_data.sql
```

**Usuários de teste:**
| E-mail                    | Senha     |
|---------------------------|-----------|
| admin@quimiochat.com      | admin123  |
| joao@quimiochat.com       | admin123  |
| maria@quimiochat.com      | admin123  |

> ⚠️ Os hashes nos dados de teste correspondem à senha `admin123`. Em produção, use o endpoint `/auth/register`.

---

## 📐 Documentação Acadêmica

| Documento                                         | Descrição                          |
|---------------------------------------------------|------------------------------------|
| [`docs/modelo_logico.md`](docs/modelo_logico.md) | Modelo lógico com DER e atributos  |
| [`docs/modelo_fisico.sql`](docs/modelo_fisico.sql)| Modelo físico SQL completo         |
| [`docs/API_DOCUMENTATION.md`](docs/API_DOCUMENTATION.md) | Documentação de todos os endpoints |

---

## 🔐 Segurança Implementada

- **Hash bcrypt** para senhas (salt único por usuário)
- **JWT HS256** com expiração configurável
- **Pydantic** para validação rigorosa de entradas
- **Variáveis sensíveis** isoladas no `.env`
- **Senhas nunca retornadas** nas respostas da API
- **HTTPS** recomendado em produção

---

## 🧪 Exemplo de Uso

### 1. Registrar usuário
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"nome":"João","email":"joao@test.com","senha":"senha123"}'
```

### 2. Fazer login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"joao@test.com","senha":"senha123"}'
# → Copie o "access_token" retornado
```

### 3. Pesquisar molécula
```bash
curl -X POST http://localhost:8000/molecules/search \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"molecule_name":"Aspirina"}'
```

**Resposta:**
```json
{
  "molecule": "Aspirina",
  "search_id": 1,
  "ai": {
    "name":    "Ácido acetilsalicílico",
    "smiles":  "CC(=O)Oc1ccccc1C(=O)O",
    "time_ms": 1842
  },
  "pubchem": {
    "cid":     2244,
    "name":    "2-(acetyloxy)benzoic acid",
    "smiles":  "CC(=O)Oc1ccccc1C(=O)O",
    "time_ms": 312
  }
}
```

---

## 🛠️ Comandos Úteis

```bash
# Verificar status da API
curl http://localhost:8000/health

# Ver logs do backend (uvicorn imprime no terminal)

# Acessar banco SQLite diretamente
sqlite3 backend/quimiochat.db
> .tables
> SELECT * FROM vw_historico_completo LIMIT 5;
> .quit

# Verificar modelos Ollama disponíveis
ollama list

# Atualizar Gemma2
ollama pull gemma2
```

---

## 👥 Contribuição

Este projeto foi desenvolvido como TCC de An�lise e Desenvolvimento de Sistemas.

---

## 📄 Licença

MIT License — Livre para uso acadêmico e educacional.
