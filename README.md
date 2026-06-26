# 🧪 Sistema de Quimioinformática Inteligente

> **Trabalho de Conclusão de Curso (TCC)**
> **Curso:** Análise e Desenvolvimento de Sistemas

---

# 📖 Sobre o Projeto

O **Sistema de Quimioinformática Inteligente** é uma aplicação web desenvolvida para integrar Inteligência Artificial Generativa com bases oficiais de dados químicos, permitindo a pesquisa de moléculas utilizando nomes populares em português.

O sistema realiza consultas simultâneas utilizando um modelo de IA local (Ollama/Gemma2) e a API pública do PubChem, comparando os resultados obtidos, o tempo de resposta de cada fonte e armazenando todas as pesquisas realizadas em banco de dados.

Além disso, a aplicação possui autenticação segura utilizando JWT, histórico de pesquisas e arquitetura baseada no padrão MVC.

---

# 🎯 Objetivos

* Facilitar a pesquisa de moléculas químicas.
* Traduzir nomes populares para nomenclatura científica.
* Gerar automaticamente representações químicas no formato SMILES.
* Comparar resultados entre Inteligência Artificial e banco oficial PubChem.
* Armazenar o histórico das pesquisas realizadas.
* Demonstrar a aplicação prática de IA Generativa na área da Quimioinformática.

---

# 🚀 Tecnologias Utilizadas

## Backend

* Python 3.11
* FastAPI
* SQLAlchemy
* Pydantic
* JWT
* bcrypt

## Frontend

* Streamlit

## Banco de Dados

* SQLite

## Inteligência Artificial

* Ollama
* Gemma2

## API Externa

* PubChem API

---

# 🏛 Arquitetura

O projeto foi desenvolvido utilizando o padrão arquitetural **MVC (Model-View-Controller)**.

A aplicação está dividida em três camadas principais:

### Frontend

Responsável pela interação com o usuário utilizando Streamlit.

### Backend

Responsável por:

* autenticação;
* regras de negócio;
* comunicação com IA;
* comunicação com PubChem;
* persistência dos dados.

### Banco de Dados

Armazena:

* usuários;
* moléculas;
* pesquisas;
* resultados da IA;
* resultados do PubChem.

---

# 📁 Estrutura do Projeto

```text
TCC_Quimiochat_IA/

backend/
frontend/
database/
docs/
README.md
```

---

# ⚙️ Principais Funcionalidades

* Cadastro de usuários
* Login seguro utilizando JWT
* Pesquisa de moléculas por nome popular
* Tradução automática utilizando IA
* Geração de estrutura SMILES
* Consulta paralela na API PubChem
* Comparação entre IA e PubChem
* Medição do tempo de resposta das consultas
* Histórico de pesquisas
* Persistência em banco SQLite

---

# 🔄 Fluxo da Aplicação

```text
Usuário

↓

Frontend (Streamlit)

↓

Backend (FastAPI)

↓

Consulta Paralela

├── Ollama (Gemma2)
└── PubChem API

↓

Comparação dos Resultados

↓

Banco SQLite

↓

Resposta ao Usuário
```

---

# 🗄 Banco de Dados

O sistema utiliza **SQLite** como banco de dados relacional.

As tabelas armazenam informações referentes a:

* Usuários
* Moléculas
* Histórico de pesquisas
* Resultado da IA
* Resultado do PubChem

O banco é criado automaticamente na primeira execução da aplicação.

---

# ▶️ Como Executar o Projeto

## 1. Clonar o repositório

```bash
git clone https://github.com/Alessandro-011/Quimiochat_IA.git
```

Entre na pasta do projeto:

```bash
cd Quimiochat_IA
```

---

# 🤖 Configurar o Ollama

Instalar o modelo:

```bash
ollama pull gemma2
```

Iniciar o servidor:

```bash
ollama serve
```

---

# 🖥 Executar o Backend

Entre na pasta:

```bash
cd backend
```

Criar ambiente virtual:

```bash
python -m venv venv
```

Ativar ambiente virtual

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Instalar dependências

```bash
pip install -r requirements.txt
```

Executar a API

```bash
uvicorn app.main:app --reload
```

A API ficará disponível em:

```
http://localhost:8000
```

Documentação automática (Swagger):

```
http://localhost:8000/docs
```

---

# 💻 Executar o Frontend

Abra um novo terminal.

Execute:

```bash
streamlit run frontend/streamlit_app.py
```

O sistema ficará disponível em:

```
http://localhost:8501
```

---

# 📚 Documentação

A pasta **docs/** contém toda a documentação complementar do projeto.

Incluindo:

* DER
* Modelo Lógico
* Modelo Físico
* Documentação da API

---

# 🔐 Segurança

O sistema utiliza:

* JWT para autenticação
* bcrypt para criptografia de senhas
* SQLAlchemy ORM
* Validação utilizando Pydantic
* Controle de acesso às rotas protegidas

---

# 📊 Arquitetura Utilizada

* MVC (Model-View-Controller)
* API REST
* Programação Assíncrona
* ORM com SQLAlchemy
* Autenticação Stateless utilizando JWT

---

# 👨‍💻 Desenvolvido para

**Trabalho de Conclusão de Curso**

Curso de **Análise e Desenvolvimento de Sistemas**

---

# 📄 Licença

Projeto desenvolvido exclusivamente para fins acadêmicos.

Todos os direitos reservados aos autores.
