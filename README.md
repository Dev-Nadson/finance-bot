# 💸 Finance Bot

**Bot de finanças pessoais para Telegram com suporte a IA, gráficos e controle de receitas e despesas.**

---

## 📋 TODO — Finance Bot

---

### 🤖 Frontend (Bot — Comandos & Handlers)

**Setup inicial**
- [ ] Criar handler de `/start` com mensagem de boas-vindas e menu de comandos
- [ ] Criar função para inserir o usuário no banco de dados no primeiro `/start`

**Geral**aiosqlite
- [ ] `/saldo` — buscar e exibir saldo atual (receitas - despesas)

**Despesas**
- [ ] `/despesa` — listar todas as despesas do usuário
- [ ] `/despesa-new <valor> <categoria> [descrição]` — registrar nova despesa via linha única
- [ ] `/despesa-edit <id> <campo> <novo_valor>` — editar despesa existente
- [ ] `/despesa-remove <id>` — remover despesa por ID

**Receitas**
- [ ] `/receita` — listar todas as receitas do usuário
- [ ] `/receita-new <valor> <categoria> [descrição]` — registrar nova receita
- [ ] `/receita-edit <id> <campo> <novo_valor>` — editar receita existente
- [ ] `/receita-remove <id>` — remover receita por ID

**Gráficos**
- [ ] `/geral` — gráfico geral com saldo, total gasto e total de despesas
- [ ] `/geral-despesa` — gráfico de pizza/barra por categoria de despesa
- [ ] `/geral-receita` — gráfico de pizza/barra por categoria de receita

**Comandos com IA**
- [ ] `/resumo` — resumo financeiro do mês gerado por IA
- [ ] `/exportar` — exportar relatório financeiro em PDF ou texto

**Validação & Erros**
- [ ] Criar função `parse_args()` com `shlex` + Pydantic para todos os comandos de entrada
- [ ] Padronizar mensagens de erro com formato de ajuda inline (ex: `❌ Use: /despesa-new 100 energia fixo`)
- [ ] Adicionar `try/except` em todos os handlers com feedback ao usuário

---

### 🗄️ Backend (Banco de Dados, Modelos & Serviços)

**Configuração do ambiente**
- [X] Adicionar `sqlalchemy`, `alembic` e ao `pyproject.toml`
- [X] Adicionar `SQL_ALCHEMY_DATABASE_URL` ao `.env.example` e ao modelo `envConfig`
- [X] Criar `database/connection.py` — engine, `SessionLocal` e `Base`

**Models**
- [ ] `database/models/user.py` — `id`, `telegram_id` (BigInteger, unique), `username`, `first_name`, `created_at`
- [ ] `database/models/despesa.py` — `id`, `user_id` (FK), `valor`, `categoria`, `descricao`, `created_at`
- [ ] `database/models/receita.py` — `id`, `user_id` (FK), `valor`, `categoria`, `descricao`, `created_at`

**Repositories (CRUD)**
- [ ] `database/repositories/user_repo.py` — `get and create(telegram_id)`
- [ ] `database/repositories/despesa_repo.py` — `create`, `list_by_user`, `update`, `delete`
- [ ] `database/repositories/receita_repo.py` — `create`, `list_by_user`, `update`, `delete`

**Migrations com Alembic**
- [ ] Inicializar Alembic (`alembic init alembic/`)
- [ ] Configurar `alembic.ini` e `env.py` para ler `DATABASE_URL` do `.env`
- [ ] Gerar migration inicial com todos os models
- [ ] Adicionar `task migrate` e `task migrate-new` no `pyproject.toml`

**Serviços**
- [ ] `services/financeiro.py` — `calcular_saldo(user_id)`, `total_por_categoria(user_id)`, `resumo_mensal(user_id)`
- [ ] `services/charts.py` — refatorar para receber dados reais do banco em vez de `x` e `y` hardcoded
- [ ] `services/ai/base.py` — interface abstrata `AIProvider`
- [ ] `services/ai/groq_provider.py` — implementação Groq
- [ ] `services/ai/openai_provider.py` — implementação OpenAI
- [ ] Remover `print()` de teste dos arquivos `groq_config.py` e `openapi_config.py`

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
| `/start` | Inicia o bot e exibe o menu principal |
| `/saldo` | Exibe o saldo atual (receitas − despesas) |
| `/resumo` | Resumo financeiro do mês gerado por IA |
| `/exportar` | Exporta relatório financeiro |

### 📉 Despesas
| Comando | Descrição |
|---|---|
| `/despesa` | Lista todas as despesas |
| `/despesa-new <valor> <categoria> [descrição]` | Cadastra uma nova despesa |
| `/despesa-edit <id> <campo> <novo_valor>` | Edita uma despesa existente |
| `/despesa-remove <id>` | Remove uma despesa |

> Exemplo: `/despesa-new 150 alimentação "mercado da semana"`

### 📈 Receitas
| Comando | Descrição |
|---|---|
| `/receita` | Lista todas as receitas |
| `/receita-new <valor> <categoria> [descrição]` | Cadastra uma nova receita |
| `/receita-edit <id> <campo> <novo_valor>` | Edita uma receita existente |
| `/receita-remove <id>` | Remove uma receita |

> Exemplo: `/receita-new 3000 salário "pagamento mensal"`

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
│   │   ├── app.py                      # Registro de handlers do bot
│   │   ├── setup.py                    # Inicialização da instância do TeleBot
│   │   └── commands/
│   │       └── v1/
│   │           ├── __init__.py         # Exporta os handlers da versão 1
│   │           ├── start_help.py       # Handler do comando /start
│   │           └── send_chart.py       # Handler do comando /chart
│   ├── config/
│   │   ├── libs/
│   │   │   ├── envroinments.py         # Carrega variáveis de ambiente com dotenv
│   │   │   ├── groq_config.py          # Configuração e cliente da API Groq
│   │   │   └── openapi_config.py       # Configuração e cliente da API OpenAI
│   │   └── schemas/
│   │       └── classes.py              # Modelos Pydantic (ex: envConfig)
│   └── services/
│       └── charts.py                   # Geração de gráficos com Matplotlib
├── .env.example                        # Exemplo de variáveis de ambiente
├── .gitignore
├── .python-version                     # Versão do Python (3.12)
├── pyproject.toml                      # Dependências e configurações do projeto
└── README.md
```

---

## 🏗️ Arquitetura

O projeto segue uma separação clara de responsabilidades dividida em três camadas principais:

**`bot/`** — Camada de interface com o Telegram. O arquivo `setup.py` instancia o `TeleBot` de forma centralizada, evitando importações circulares. O arquivo `app.py` registra os handlers e os conecta aos comandos. Os comandos ficam organizados por versão dentro de `commands/v1/`.

**`config/`** — Camada de configuração e infraestrutura. Carrega as variáveis de ambiente via `dotenv`, valida-as com um modelo Pydantic (`envConfig`) e expõe clientes prontos para uso das APIs externas (Groq e OpenAI).

**`services/`** — Camada de lógica e serviços reutilizáveis. Atualmente contém a geração de gráficos com Matplotlib. Aqui ficarão os serviços de IA, relatórios e regras de negócio financeiras.

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
SQL_ALCHEMY_DATABASE_URL=caminho_do_banco
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
| `SQL_ALCHEMY_DATABASE_URL` | Caminho do banco de dados SQLite |
| `TELEGRAM_BOT_TOKEN` | Token do bot gerado pelo [@BotFather](https://t.me/BotFather) |
| `GROQ_API_KEY` | Chave de acesso à API da [Groq](https://console.groq.com/) |
| `OPENAI_API_KEY` | Chave de acesso à API da [OpenAI](https://platform.openai.com/) |

---

## 🛠️ Tecnologias

- **[pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)** — Interface com a API do Telegram
- **[Matplotlib](https://matplotlib.org/)** — Geração de gráficos
- **[Groq](https://groq.com/)** — Inferência de IA de alta velocidade (LLaMA)
- **[OpenAI](https://openai.com/)** — Integração com modelos GPT
- **[Pydantic](https://docs.pydantic.dev/)** — Validação de configurações
- **[uv](https://docs.astral.sh/uv/)** — Gerenciamento de dependências e ambiente virtual
- **[Ruff](https://docs.astral.sh/ruff/)** — Linter e formatter Python
