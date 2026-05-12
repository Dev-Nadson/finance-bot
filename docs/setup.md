# ⚙️ Instalação e Configuração

Siga este guia para configurar o ambiente de desenvolvimento e executar o **Finance Bot**.

## Pré-requisitos

Antes de começar, certifique-se de ter instalado:
- **Python 3.12+**
- **[uv](https://docs.astral.sh/uv/)** (Gerenciador de pacotes ultra-rápido para Python)

## Passo a Passo

### 1. Clonar o Repositório
```bash
git clone https://github.com/seu-usuario/finance-bot.git
cd finance-bot
```

### 2. Instalar Dependências
Utilize o `uv` para criar o ambiente virtual e instalar todas as dependências necessárias:
```bash
uv sync
```

### 3. Configurar Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto copiando o exemplo:
```bash
cp .env.example .env
```

Edite o arquivo `.env` e preencha as suas chaves:
```env
SQL_ALCHEMY_DATABASE_URL=sqlite+aiosqlite:///database.db
TELEGRAM_BOT_TOKEN=seu_token_aqui
GROQ_API_KEY=sua_chave_groq_aqui
OPENAI_API_KEY=sua_chave_openai_aqui
```

### 4. Inicializar o Banco de Dados
Execute o script de setup para criar as tabelas necessárias no SQLite:
```bash
uv run setup_db.py
```

### 5. Executar o Bot
Com tudo configurado, inicie o bot:
```bash
uv run src/main.py
```

## Ferramentas de Desenvolvimento

### Linting e Formatação
O projeto utiliza **Ruff** para garantir a qualidade do código. Você pode rodar as tarefas através do `taskipy`:

- **Verificar problemas**: `uv run task lint`
- **Corrigir automaticamente**: `uv run task lint-fix`
- **Formatar o código**: `uv run task lint-format`
