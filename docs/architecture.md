# 🏗️ Arquitetura e Estrutura

O **Finance Bot** foi projetado com foco em modularidade e separação de responsabilidades, facilitando a expansão de funcionalidades e a manutenção do código.

---

## Padrões de Projeto

O sistema segue uma arquitetura em camadas:

| Camada | Localização | Responsabilidade |
|---|---|---|
| **Interface (Bot)** | `src/bot/` | Comunicação com a API do Telegram, registro de handlers |
| **Controladores** | `src/services/controllers/` | Fluxo de conversas (`ConversationHandler`) e lógica de decisão |
| **Repositórios** | `src/services/repositories/` | Abstração das consultas ao banco de dados |
| **Modelos** | `src/database/models/` | Definição das tabelas via SQLAlchemy |
| **Configuração** | `src/config/` | Variáveis de ambiente e clientes de terceiros (OpenAI, Groq) |
| **Web** | `src/web/` | Dashboard Flask com gráficos e insights de IA |
| **Relatórios** | `src/services/reports/` | Geração de gráficos com Matplotlib |

---

## Estrutura de Pastas

```text
finance-bot/
├── docker-compose.yml              # PostgreSQL via Bitnami
├── docs/                           # Documentação do projeto (MkDocs)
├── src/
│   ├── main.py                     # Ponto de entrada do bot Telegram
│   ├── bot/
│   │   ├── app.py                  # Registro de todos os handlers
│   │   └── commands/
│   │       ├── backend/            # Comandos de lógica (saldo, gráficos, IA)
│   │       └── frontend/           # Comandos de UI (menu, help)
│   ├── config/
│   │   ├── libs/
│   │   │   ├── openapi_config.py   # Cliente OpenAI (ativo)
│   │   │   ├── groq_config.py      # Cliente Groq (reservado para uso futuro)
│   │   │   └── envroinments.py     # Carregamento e validação do .env
│   │   └── schemas/                # Schemas Pydantic para gráficos
│   ├── database/
│   │   └── models/
│   │       ├── db_config.py        # Engine e SessionLocal (asyncpg)
│   │       ├── t01_users.py        # Modelo: usuários Telegram
│   │       ├── t02_accounts.py     # Modelo: contas financeiras
│   │       ├── t03_users_accounts.py # Relação N:N usuários-contas
│   │       ├── t04_expenses.py     # Modelo: despesas
│   │       └── t05_incomes.py      # Modelo: receitas
│   ├── services/
│   │   ├── controllers/            # Lógica de negócio e diálogos do bot
│   │   │   ├── account_controller.py
│   │   │   ├── expense_controller.py
│   │   │   ├── income_controller.py
│   │   │   ├── login_controller.py
│   │   │   └── ai_controller.py    # Relatório financeiro via IA (async)
│   │   ├── repositories/           # Camada de persistência
│   │   │   ├── accounts_repository.py
│   │   │   ├── expenses_repository.py
│   │   │   └── incomes_repository.py
│   │   ├── financeiro.py           # Cálculos: saldo, categorias, evolução
│   │   └── reports/
│   │       └── charts.py           # Geração de gráficos (pizza, linhas)
│   └── web/
│       ├── app.py                  # Flask — Dashboard web
│       └── templates/
│           └── index.html          # Interface do dashboard
├── pyproject.toml                  # Dependências e configuração do projeto
└── README.md                       # Guia rápido de execução
```

---

## Banco de Dados

O projeto utiliza **PostgreSQL** com o driver assíncrono **asyncpg**.
As tabelas são gerenciadas pelo SQLAlchemy ORM e criadas via `Base.metadata.create_all`.

### Schema das Tabelas

```
users           → id, telegram_id, created_at
accounts        → id, name, password (bcrypt hash), created_at
users_accounts  → user_id (FK), account_id (FK)
expenses        → id, account_id, user_id, value, type, category, description, competencia, created_at
incomes         → id, account_id, user_id, value, type, category, description, competencia, created_at
```

> **`competencia`**: Campo no formato `YYYY-MM` que representa o mês de competência financeira do lançamento, independente da data de criação.

---

## Segurança

- **Senhas** armazenadas com **bcrypt** (salt aleatório por conta).
- **Isolamento de dados**: todos os repositórios verificam `telegram_id` e `account_id` antes de qualquer operação.
- **Variáveis sensíveis** gerenciadas via `.env`, nunca commitadas no repositório.

---

## Tecnologias

| Tecnologia | Versão | Uso |
|---|---|---|
| Python | 3.12+ | Linguagem principal |
| python-telegram-bot | 22+ | Framework do bot Telegram |
| SQLAlchemy | 2.x (async) | ORM e gerenciamento de banco |
| PostgreSQL + asyncpg | latest | Banco de dados principal |
| Docker / Bitnami | latest | Containerização do banco |
| OpenAI | 2.x | Geração de relatórios com IA |
| Flask | 3.x | Dashboard web |
| Matplotlib | 3.x | Geração de gráficos |
| bcrypt | 5.x | Hash seguro de senhas |
| uv | latest | Gerenciamento de dependências |
| Ruff | latest | Linting e formatação |
