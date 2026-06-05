# 💸 Finance Bot

**Bot de finanças pessoais para Telegram com suporte a IA, gráficos e controle de contas, receitas e despesas.**

---

## 🚀 Guia Rápido

Para começar a usar o bot localmente, siga os passos abaixo:

### Pré-requisitos
- **Python 3.12+**
- **[uv](https://docs.astral.sh/uv/)** — gerenciador de pacotes
- **[Docker](https://docs.docker.com/get-docker/)** — para o banco de dados PostgreSQL

---

### 1. Clonar e instalar dependências
```bash
git clone https://github.com/seu-usuario/finance-bot.git
cd finance-bot
uv sync
```

### 2. Configurar variáveis de ambiente
```bash
cp .env.example .env
# Edite o .env com seu TELEGRAM_BOT_TOKEN, OPENAI_API_KEY e credenciais do banco
```

Exemplo de `.env`:
```env
SQL_ALCHEMY_DATABASE_URL=postgresql+asyncpg://finance_user:finance_pass@localhost:5432/finance_db
TELEGRAM_BOT_TOKEN=seu_token_aqui
GROQ_API_KEY=sua_chave_groq_aqui
OPENAI_API_KEY=sua_chave_openai_aqui
```

### 3. Subir o banco de dados (PostgreSQL via Docker)
```bash
docker compose up -d
```

### 4. Inicializar as tabelas
```bash
uv run src/setup_db.py
```

### 5. Executar o bot
```bash
uv run src/main.py
```

---

## 🌐 Dashboard Web

O projeto inclui um painel web para visualização de gráficos e insights de IA:

```bash
uv run src/web/app.py
# Acesse: http://localhost:5000
```

---

## 🛠️ Ferramentas de Desenvolvimento

```bash
uv run task lint          # Verificar problemas de código
uv run task lint-fix      # Corrigir automaticamente
uv run task lint-format   # Formatar o código
```

---

## 📖 Documentação Completa

Para informações detalhadas sobre a arquitetura, estrutura de pastas e funcionalidades:

👉 **[Documentação Completa (Docs)](docs/index.md)**

*(Ou execute `uv run mkdocs serve` para visualizar no navegador)*
