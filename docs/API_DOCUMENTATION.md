# API Documentation — Sistema de Quimioinformática Inteligente

**Versão:** 1.0.0  
**Base URL:** `http://localhost:8000`  
**Documentação Interativa:** `http://localhost:8000/docs` (Swagger UI)  
**Documentação Alternativa:** `http://localhost:8000/redoc`

---

## Autenticação

A API usa **JWT Bearer Token**. Após o login, inclua o token no header:

```
Authorization: Bearer <seu_token_jwt>
```

---

## 1. Health Check

### `GET /`
Verificação básica de status da API.

**Resposta 200:**
```json
{
  "status": "online",
  "sistema": "Sistema de Quimioinformática Inteligente",
  "versao": "1.0.0",
  "docs": "/docs",
  "redoc": "/redoc"
}
```

---

### `GET /health`
Health check detalhado dos serviços.

**Resposta 200:**
```json
{
  "api": "online",
  "banco": "online",
  "ollama": "online"
}
```

---

## 2. Autenticação (`/auth`)

### `POST /auth/register`
Registra um novo usuário no sistema.

**Request Body:**
```json
{
  "nome":  "João Silva",
  "email": "joao@exemplo.com",
  "senha": "minhasenha123"
}
```

**Resposta 201 (Criado):**
```json
{
  "id":         1,
  "nome":       "João Silva",
  "email":      "joao@exemplo.com",
  "created_at": "2025-01-15T10:30:00"
}
```

**Resposta 409 (Conflito):**
```json
{
  "detail": "Este e-mail já está cadastrado."
}
```

**Resposta 422 (Validação):**
```json
{
  "detail": [
    { "loc": ["body", "email"], "msg": "value is not a valid email address" }
  ]
}
```

---

### `POST /auth/login`
Autentica o usuário e retorna o token JWT.

**Request Body:**
```json
{
  "email": "joao@exemplo.com",
  "senha": "minhasenha123"
}
```

**Resposta 200 (OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type":   "bearer",
  "user": {
    "id":         1,
    "nome":       "João Silva",
    "email":      "joao@exemplo.com",
    "created_at": "2025-01-15T10:30:00"
  }
}
```

**Resposta 401 (Não autorizado):**
```json
{
  "detail": "E-mail ou senha incorretos."
}
```

---

## 3. Moléculas (`/molecules`) 🔒 *Requer JWT*

### `GET /molecules`
Lista todas as moléculas cadastradas com paginação.

**Query Parameters:**
| Parâmetro | Tipo    | Padrão | Descrição             |
|-----------|---------|--------|-----------------------|
| skip      | integer | 0      | Registros para pular  |
| limit     | integer | 50     | Máximo de resultados  |

**Resposta 200:**
```json
[
  {
    "id":            1,
    "nome_original": "Aspirina",
    "nome_quimico":  "Ácido acetilsalicílico",
    "smiles":        "CC(=O)Oc1ccccc1C(=O)O"
  },
  {
    "id":            2,
    "nome_original": "Cafeína",
    "nome_quimico":  "1,3,7-trimetilxantina",
    "smiles":        "Cn1c(=O)c2c(ncn2C)n(c1=O)C"
  }
]
```

---

### `GET /molecules/{molecule_id}`
Busca uma molécula específica pelo ID.

**Path Parameters:**
| Parâmetro   | Tipo    | Descrição        |
|-------------|---------|------------------|
| molecule_id | integer | ID da molécula   |

**Resposta 200:**
```json
{
  "id":            1,
  "nome_original": "Aspirina",
  "nome_quimico":  "Ácido acetilsalicílico",
  "smiles":        "CC(=O)Oc1ccccc1C(=O)O",
  "created_at":    "2025-01-15T10:30:00"
}
```

**Resposta 404:**
```json
{
  "detail": "Molécula com ID 99 não encontrada."
}
```

---

### `POST /molecules/search` ⭐ *Rota principal do TCC*
Pesquisa uma molécula consultando IA (Ollama/Gemma2) e PubChem em paralelo.

> ⚠️ **Atenção:** Esta rota pode levar até 2 minutos para responder, pois aguarda o Ollama processar o prompt.

**Request Body:**
```json
{
  "molecule_name": "Aspirina"
}
```

**Resposta 200:**
```json
{
  "molecule":  "Aspirina",
  "search_id": 42,
  "ai": {
    "name":    "Aspirin",
    "smiles":  "CC(=O)Oc1ccccc1C(=O)O",
    "time_ms": 1842
  },
  "pubchem": {
    "cid":              2244,
    "nome_comum":       "Aspirin",
    "nome_iupac":       "2-(acetyloxy)benzoic acid",
    "smiles_canonico":  "CC(=O)OC1=CC=CC=C1C(=O)O",
    "smiles_isomerico": "CC(=O)OC1=CC=CC=C1C(=O)O",
    "formula":          "C9H8O4",
    "massa":            "180.16",
    "time_ms":          312
  }
}
```

**Campos da resposta:**

| Campo                      | Tipo    | Descrição                                        |
|----------------------------|---------|--------------------------------------------------|
| molecule                   | string  | Nome pesquisado                                  |
| search_id                  | integer | ID do registro salvo no banco                    |
| ai.name                    | string  | Nome químico traduzido pelo Gemma2               |
| ai.smiles                  | string  | SMILES gerado pela IA                            |
| ai.time_ms                 | integer | Tempo de resposta da IA em milissegundos         |
| pubchem.cid                | integer | PubChem Compound ID                              |
| pubchem.nome_comum         | string  | Nome oficial/Title no PubChem                    |
| pubchem.nome_iupac         | string  | Nomenclatura IUPAC oficial                       |
| pubchem.smiles_canonico    | string  | SMILES canônico oficial da base                  |
| pubchem.smiles_isomerico   | string  | SMILES isomérico estrutural da base              |
| pubchem.formula            | string  | Fórmula molecular exata                          |
| pubchem.massa              | string  | Massa molecular em g/mol                         |
| pubchem.time_ms            | integer | Tempo de resposta do PubChem em milissegundos    |

---

### `POST /molecules`
Cria uma molécula manualmente (sem pesquisa por IA).

**Request Body:**
```json
{
  "nome_original": "Etanol",
  "nome_quimico":  "Álcool etílico",
  "smiles":        "CCO"
}
```

**Resposta 201:**
```json
{
  "id":            10,
  "nome_original": "Etanol",
  "nome_quimico":  "Álcool etílico",
  "smiles":        "CCO",
  "created_at":    "2025-01-15T14:00:00"
}
```

---

### `DELETE /molecules/{molecule_id}`
Remove uma molécula do banco pelo ID.

**Resposta 200:**
```json
{
  "message": "Molécula 'Etanol' removida com sucesso."
}
```

---

## 4. Histórico de Pesquisas (`/search`) 🔒 *Requer JWT*

### `GET /search/history`
Retorna o histórico de pesquisas do usuário autenticado.

**Query Parameters:**
| Parâmetro | Tipo    | Padrão | Descrição             |
|-----------|---------|--------|-----------------------|
| skip      | integer | 0      | Registros para pular  |
| limit     | integer | 20     | Máximo de resultados  |

**Resposta 200:**
```json
[
  {
    "id":               1,
    "search_time":      "2025-01-15T10:30:00",
    "response_time_ms": 1250,
    "molecule":         "Aspirina",
    "ai_name":          "Ácido acetilsalicílico",
    "ai_smiles":        "CC(=O)Oc1ccccc1C(=O)O",
    "ai_time_ms":       1100,
    "pubchem_name":     "2-(acetyloxy)benzoic acid",
    "pubchem_smiles":   "CC(=O)Oc1ccccc1C(=O)O",
    "pubchem_time_ms":  150
  }
]
```

---

## Códigos de Status HTTP

| Código | Significado                                           |
|--------|-------------------------------------------------------|
| 200    | OK — Requisição processada com sucesso                |
| 201    | Created — Recurso criado com sucesso                  |
| 401    | Unauthorized — Token ausente, inválido ou expirado    |
| 404    | Not Found — Recurso não encontrado                    |
| 409    | Conflict — Dados duplicados (e-mail ou nome)          |
| 422    | Unprocessable Entity — Falha de validação Pydantic    |
| 500    | Internal Server Error — Erro interno do servidor      |

---

## Exemplo de Uso com cURL

### Login:
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@quimiochat.com", "senha": "admin123"}'
```

### Pesquisar Molécula:
```bash
curl -X POST http://localhost:8000/molecules/search \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -d '{"molecule_name": "Aspirina"}'
```

### Histórico:
```bash
curl -X GET http://localhost:8000/search/history \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```
