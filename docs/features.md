# 🚀 Funcionalidades

O **Finance Bot** oferece um conjunto completo de ferramentas para o controle financeiro pessoal diretamente pelo Telegram.

---

## 🤖 Interface do Bot (Telegram)

### Comandos Disponíveis

| Comando | Descrição |
|---|---|
| `/start` | Inicia o bot e exibe boas-vindas |
| `/menu` | Exibe o menu principal interativo |
| `/help` | Lista todos os comandos disponíveis |
| `/new_account` | Cria uma nova conta financeira |
| `/login_account` | Faz login em uma conta existente |
| `/new_expense` | Registra uma nova despesa |
| `/new_income` | Registra uma nova receita |
| `/saldo` | Exibe o saldo atual da conta ativa |
| `/chart` | Gráfico de evolução mensal de saldo/despesas |
| `/chart2` | Gráfico de pizza — despesas por categoria |
| `/analise` | Relatório financeiro inteligente gerado por IA |

---

### Gerenciamento de Dados (CRUD)

- **Contas**: Crie e gerencie contas financeiras protegidas por senha (bcrypt).
- **Despesas**: Registre gastos com categoria (Alimentação, Lazer, Necessidades Básicas), valor e descrição.
- **Receitas**: Registre entradas financeiras com tipo e descrição.
- **Edição e Exclusão**: Edite ou remova despesas e receitas existentes pelo ID.

### Competência Financeira

Todos os lançamentos utilizam um campo `competencia` (`YYYY-MM`) que representa o **mês de referência** do lançamento, independente da data em que foi criado. Isso permite filtrar despesas e receitas por mês de forma precisa.

---

## 📊 Dashboard Web

Acesse em `http://localhost:5000` após executar `uv run src/web/app.py`.

### Painel de Resumo
- **Receitas do mês** — total de entradas do mês atual
- **Despesas do mês** — total de saídas do mês atual
- **Saldo** — diferença entre receitas e despesas com barra de progresso visual

### Gráficos
- **Evolução de Receitas** — gráfico de linhas com os últimos 6 meses
- **Evolução de Despesas** — gráfico de linhas com os últimos 6 meses
- **Por Categoria** — gráfico de pizza com dois modos:
  - **Mês Atual** — filtra pelo mês vigente
  - **Todo Período** — exibe o acumulado geral

### Insights de IA
- Relatório gerado automaticamente pela OpenAI ao carregar o dashboard.
- Analisa receitas, despesas e categorias do mês atual.
- Fornece dicas práticas de economia e investimento.

---

## 🔒 Segurança

- **Senhas hasheadas** com bcrypt — nunca armazenadas em texto puro.
- **Isolamento de dados** — cada usuário acessa apenas as contas vinculadas ao seu `telegram_id`.
- **Credenciais** gerenciadas via variáveis de ambiente.

---

## 🤖 Inteligência Artificial

- Relatórios financeiros mensais gerados pela **OpenAI (GPT-4o-mini)**.
- Integração **assíncrona** via `asyncio.to_thread` — sem bloqueio do event loop do bot.
- Análise de receitas, despesas totais e distribuição por categoria.
- Retorno formatado em HTML para exibição no Telegram e no dashboard web.
