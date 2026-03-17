# 💸 Finance Bot

**Bot de finanças pessoais para Telegram com suporte a IA, gráficos e controle de receitas e despesas.**

---

## 📋 To-Do List

### ✅ Essencial

- [ ] Iniciar o bot e mostrar menu principal
- [ ] Registrar despesa
- [ ] Registrar receita
- [ ] Calcular saldo atual

### 🔧 Comandos Fixos

- [ ] Exibir comandos de registro
- [ ] Listar transações
- [ ] Filtrar por período
- [ ] Filtrar por categoria
- [ ] Total de receitas e despesas
- [ ] Categoria com maior gasto
- [ ] Gráfico de evolução de gastos
- [ ] Editar e excluir transação
- [ ] Histórico recente

### 🤖 Comandos com IA

- [ ] Gráfico de gastos por categoria
- [ ] Gráfico comparativo receitas x despesas
- [ ] Resumo financeiro do mês
- [ ] Exportar relatório financeiro

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
│   │   └── models/
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

## 🚀 Guia de Comandos

| Comando | Descrição |
|---|---|
| Geral | Comandos gerais |
| `/saldo` | Saldo disponível após as despesas |
|---|---|
| Despesas | Comandos para manipular as despesas |
| `/despesa` | Lista todas as despesas |
| `/despesa-new` | Cadastra uma nova despesa |
| `/despesa-edit` | Edita uma despesa existente |
| `/despesa-remove` | Remove uma despesa |
|---|---|
| Receita | Comandos para manipular as fontes de receita |
| `/receita` | Lista todas as receitas |
| `/receita-new` | Cadastra uma nova receita |
| `/receita-edit` | Edita uma receita existente |
| `/receita-remove` | Remove uma receita |
|---|---|
| Geral | Comandos para gerar gŕaficos |
| `/geral` | Gráfico geral — Saldo, Gasto e Despesa |
| `/geral-despesa` | Gráfico de despesas por tipo de gasto |
| `/geral-receita` | Gráfico de receitas por tipo |

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
TELEGRAM_BOT_TOKEN=seu_token_aqui
GROQ_API_KEY=sua_chave_groq_aqui
OPENAI_API_KEY=sua_chave_openai_aqui
```

### 4. Execute o projeto

**Modo de desenvolvimento:**

```bash
uv run src/main.py
```

**Modo padrão:**

```bash
uv run python src/main.py
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
