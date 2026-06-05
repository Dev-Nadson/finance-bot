# ⚙️ Instalação e Configuração

Siga este guia para configurar o ambiente de desenvolvimento e executar o **Finance Bot**.

## Pré-requisitos

Antes de começar, certifique-se de ter instalado:
- **Python 3.12+**
- **[uv](https://docs.astral.sh/uv/)** — gerenciador de pacotes para Python
- **[Docker](https://docs.docker.com/get-docker/)** — para rodar o PostgreSQL em container

---

## Passo a Passo

### 1. Clonar o Repositório
```bash
git clone https://github.com/seu-usuario/finance-bot.git
cd finance-bot
```

### 2. Instalar Dependências
```bash
uv sync
```

### 3. Configurar Variáveis de Ambiente
```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais:

```env
SQL_ALCHEMY_DATABASE_URL=postgresql+asyncpg://finance_user:finance_pass@localhost:5432/finance_db
TELEGRAM_BOT_TOKEN=seu_token_aqui
GROQ_API_KEY=sua_chave_groq_aqui        # opcional
OPENAI_API_KEY=sua_chave_openai_aqui
```

> **Nota:** O `GROQ_API_KEY` é opcional e reservado para uso futuro. O bot utiliza a OpenAI por padrão.

### 4. Subir o Banco de Dados (PostgreSQL)

O projeto usa **PostgreSQL via Docker** com a imagem Bitnami. Para iniciar:

```bash
docker compose up -d
```

Isso cria um container PostgreSQL com:
- **Usuário**: `finance_user`
- **Senha**: `finance_pass`
- **Banco**: `finance_db`
- **Porta**: `5432`

Para parar o banco: `docker compose down`

### 5. Inicializar as Tabelas

Execute o comando abaixo para criar o schema do banco de dados:

```bash
uv run python -c "
import asyncio, sys
sys.path.insert(0, 'src')
from database.models.db_config import engine, Base
import database.models.t01_users
import database.models.t02_accounts
import database.models.t03_users_accounts
import database.models.t04_expenses
import database.models.t05_incomes

async def setup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print('Tabelas criadas com sucesso!')

asyncio.run(setup())
"
```

### 6. Executar o Bot
```bash
uv run src/main.py
```

### 7. (Opcional) Executar o Dashboard Web
```bash
uv run src/web/app.py
# Acesse: http://localhost:5000
```

---

## Ferramentas de Desenvolvimento

O projeto utiliza **Ruff** para garantir a qualidade do código. Execute via `taskipy`:

| Comando | Ação |
|---|---|
| `uv run task lint` | Verifica problemas de estilo |
| `uv run task lint-fix` | Corrige automaticamente |
| `uv run task lint-format` | Formata o código |
| `uv run mkdocs serve` | Visualiza a documentação no navegador |
