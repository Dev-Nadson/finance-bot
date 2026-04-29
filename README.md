# 💸 Finance Bot

**Bot de finanças pessoais para Telegram com suporte a IA, gráficos e controle de contas, receitas e despesas.**

---

## 📋 TODO — Finance Bot

---

### 🤖 Frontend (Bot — Comandos & Handlers)

**Setup inicial**
- [X] Criar handler de `/start` com mensagem de boas-vindas e menu de comandos
- [X] Criar funcionalidade para inserir o usuário no banco de dados no primeiro `/start`

**Geral**
- [X] `/menu` — Menu principal interativo
- [X] `/help` — Mensagem de ajuda detalhada
- [X] `/saldo` — Buscar e exibir saldo atual (através do controller de balanço)

**Gerenciamento de Dados (Conversations)**
- [X] Fluxo de criação/edição/remoção de **Contas**
- [X] Fluxo de criação/edição/remoção de **Despesas**
- [X] Fluxo de criação/edição/remoção de **Receitas**

**Gráficos**
- [ ] `/geral` — gráfico geral com saldo, total gasto e total de despesas
- [ ] `/geral-despesa` — gráfico de pizza/barra por categoria de despesa
- [ ] `/geral-receita` — gráfico de pizza/barra por categoria de receita

**Comandos com IA**
- [ ] `/resumo` — resumo financeiro do mês gerado por IA
- [ ] `/exportar` — exportar relatório financeiro em PDF ou texto

**Validação & Erros**
- [X] Integração de controllers com handlers do bot
- [X] Padronizar mensagens de feedback ao usuário
- [ ] Adicionar `try/except` nos controllers para tratamento de erros

---

### 🗄️ Backend (Banco de Dados, Modelos & Serviços)

**Configuração do ambiente**
- [X] Adicionar `sqlalchemy`, `alembic` e ao `pyproject.toml`
- [X] Adicionar `SQL_ALCHEMY_DATABASE_URL` ao `.env.example` e ao modelo `envConfig`
- [X] Criar `database/connection.py` — engine, `SessionLocal` e `Base`

**Models**
- [X] `database/models/users.py`
- [X] `database/models/accounts.py`
- [X] `database/models/users-accounts.py`
- [X] `database/models/expenses.py`
- [X] `database/models/incomes.py`

**Repositories (CRUD)**
- [X] `database/repositories/user_repo.py` — `get and create(telegram_id)`
- [ ] `database/repositories/despesa_repo.py` — `create`, `list_by_user`, `update`, `delete`
- [ ] `database/repositories/receita_repo.py` — `create`, `list_by_user`, `update`, `delete`

**Serviços**
- [ ] `services/financeiro.py` — `calcular_saldo(user_id)`, `total_por_categoria(user_id)`, `resumo_mensal(user_id)`
- [ ] `services/charts.py` — refatorar para receber dados reais do banco em vez de `x` e `y` hardcoded
- [ ] `services/ai/base.py` — interface abstrata `AIProvider`
- [ ] `services/ai/groq_provider.py` — implementação Groq
- [ ] `services/ai/openai_provider.py` — implementação OpenAI
- [X] Remover `print()` de teste dos arquivos `groq_config.py` e `openapi_config.py`

**Futuro (PostgreSQL + Docker)**
- [ ] Criar `Dockerfile`
- [ ] Criar `docker-compose.yml` com serviços `bot` e `postgres`
- [ ] Trocar `DATABASE_URL` de SQLite para PostgreSQL na configuração
- [ ] Substituir driver por `psycopg2` ou `asyncpg`

---

## 🚀 Guia de Comandos

### 💰 Geral
| Comando | Descrição |
|---|---|
| `/start` | Inicia o bot e exibe a mensagem de boas-vindas |
| `/menu` | Menu principal interativo (Contas, Receitas, Despesas) |
| `/help` | Guia de ajuda detalhado |
| `/saldo` | Exibe o saldo atual consolidado |

### 📊 Gráficos
| Comando | Descrição |
|---|---|
| `/geral` | Gráfico geral — Saldo, Receitas e Despesas |
| `/geral-despesa` | Gráfico de despesas por categoria |
| `/geral-receita` | Gráfico de receitas por categoria |

---

## 🗂️ Estrutura de Pastas

```
finance-bot/
├── src/
│   ├── main.py                         # Ponto de entrada da aplicação
│   ├── bot/
│   │   ├── app.py                      # Registro de todos os handlers
│   │   └── commands/                   # Lógica dos comandos separada por contexto
│   │       ├── backend/                # Comandos base (start, charts)
│   │       └── frontend/               # Menus e mensagens de ajuda
│   ├── config/
│   │   ├── libs/
│   │   │   ├── envroinments.py         # Carrega variáveis de ambiente com dotenv
│   │   │   ├── groq_config.py          # Configuração e cliente da API Groq
│   │   │   └── openapi_config.py       # Configuração e cliente da API OpenAI
│   │   └── schemas/
│   │       └── classes.py              # Modelos Pydantic (ex: envConfig)
│   └── services/
│       ├── controllers/                # Lógica de negócio e conversas (Account, Expense, etc.)
│       ├── repositories/               # Camada de acesso ao banco de dados
│       └── reports/                    # Geração de gráficos (charts.py)
├── .env.example
├── pyproject.toml
└── README.md
```

---

## 🏗️ Arquitetura

O projeto segue o padrão de **Camadas** com foco em separação de responsabilidades:

- **`bot/`**: Interface com o Telegram. Utiliza `python-telegram-bot` e organiza comandos em contextos de frontend (UI/Menus) e backend (Ações diretas).
- **`services/controllers/`**: Contém a lógica de negócio e gerencia as conversas (ConversationHandler) para entrada de dados.
- **`services/repositories/`**: Abstração da camada de dados. Realiza consultas ao banco utilizando SQLAlchemy.
- **`database/models/`**: Definições das tabelas e esquemas do banco SQLite/Postgres.
- **`config/`**: Gerenciamento de ambiente e clientes de APIs externas de forma centralizada.

---

## ⚙️ Instalação e Execução

### Pré-requisitos

- [Python 3.12+](https://www.python.org/)
- [uv](https://docs.astral.sh/uv/) instalado

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/finance-bot.git
cd finance-bot
```

### 2. Instale as dependências

```bash
uv sync
```

### 3. Configure as variáveis de ambiente

Copie o arquivo de exemplo e preencha com suas credenciais:

```bash
cp .env.example .env
```

```env
SQL_ALCHEMY_DATABASE_URL=sqlite+aiosqlite:///database.db
TELEGRAM_BOT_TOKEN=seu_token_aqui
GROQ_API_KEY=sua_chave_groq_aqui
OPENAI_API_KEY=sua_chave_openai_aqui
```

### 4. Execute o projeto

```bash
uv run src/main.py
```

### 5. Linting e formatação

```bash
# Verificar problemas
uv run task lint

# Corrigir automaticamente
uv run task lint-fix

# Formatar o código
uv run task lint-format
```

---

## 🔑 Variáveis de Ambiente

| Variável | Descrição |
|---|---|
| `SQL_ALCHEMY_DATABASE_URL` | URL de conexão com o banco de dados |
| `TELEGRAM_BOT_TOKEN` | Token do bot gerado pelo [@BotFather](https://t.me/BotFather) |
| `GROQ_API_KEY` | Chave de acesso à API da [Groq](https://console.groq.com/) |
| `OPENAI_API_KEY` | Chave de acesso à API da [OpenAI](https://platform.openai.com/) |

---

## 🛠️ Tecnologias

- **[python-telegram-bot](https://python-telegram-bot.org/)** — Framework para o bot do Telegram
- **[SQLAlchemy](https://www.sqlalchemy.org/)** — ORM para banco de dados
- **[aiosqlite](https://github.com/omnilib/aiosqlite)** — Driver assíncrono para SQLite
- **[Matplotlib](https://matplotlib.org/)** — Geração de gráficos
- **[Groq](https://groq.com/)** — Integração com Modelos de Linguagem (LLMs)
- **[OpenAI](https://openai.com/)** — Integração com Modelos de Linguagem (LLMs)
- **[Pydantic](https://docs.pydantic.dev/)** — Validação de configurações
- **[uv](https://docs.astral.sh/uv/)** — Gerenciamento de dependências ultra-rápido
- **[Ruff](https://docs.astral.sh/ruff/)** — Linter e formatter de alta performance
