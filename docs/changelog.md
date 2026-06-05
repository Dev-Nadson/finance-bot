# 📜 Histórico de Alterações (Changelog)

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

---

## 1.0.0 — 04/06/2026

### Segurança
- **Hash de senhas com bcrypt**: Senhas de contas agora são armazenadas com hash bcrypt seguro. Nenhuma senha é salva em texto puro.
- **Validação de acesso**: Todos os repositórios verificam `telegram_id` antes de qualquer operação de escrita ou leitura.

### Performance
- **Event loop não bloqueante**: Chamada à OpenAI movida para `asyncio.to_thread`, permitindo que o bot continue responsivo durante a geração de relatórios de IA.

### Funcionalidades
- **Filtro de mês no gráfico de pizza**: O dashboard web agora filtra as despesas por categoria do mês ativo, com botão para alternar para o período completo.
- **Campo `competencia`**: Todos os lançamentos financeiros utilizam o campo `YYYY-MM` para representar o mês de referência, desvinculado da data de criação.

### Infraestrutura
- **Migração para PostgreSQL**: Substituição do SQLite pelo PostgreSQL com driver assíncrono `asyncpg`.
- **Docker Compose**: Adicionado `docker-compose.yml` com imagem `bitnami/postgresql` para ambiente de banco local.
- **`asyncpg` adicionado**: Dependência `aiosqlite` removida e `asyncpg` adicionado ao `pyproject.toml`.

### Correções
- **Comando `/help` corrigido**: Lista atualizada para exibir apenas os comandos reais existentes no bot.
- **Código morto removido**: Funções legadas removidas (`create_account_repo_v1`, `delete_account_repo`, `create_expenses_repository`, `create_incomes_repository`) e variáveis não utilizadas limpas nos controllers.

---

## 0.4.0 — 03/06/2026

### Funcionalidades
- **Dashboard Web**: Painel Flask com gráficos de evolução de receitas, despesas e pizza por categoria.
- **Insights de IA no Dashboard**: Relatório financeiro inteligente carregado automaticamente ao abrir o painel.
- **Filtro de mês no saldo**: `calculate_balance` aceita filtro de `month` e `year` via `competencia`.

---

## 0.3.0 — 01/06/2026

### Funcionalidades
- **Análise de IA no Telegram**: Comando `/analise` que gera relatório financeiro mensal utilizando a OpenAI.
- **Gráficos de evolução**: Comandos `/chart` e `/chart2` para visualizar histórico financeiro.

---

## 0.2.0 — 12/05/2026

- **Página Web de Visualização**: Adição de uma página web para analisar os gráficos gerados pelo sistema e facilitar a investigação visual dos dados.

---

## 0.1.0 — 06/05/2026

- **Adição da Documentação**: Implementação inicial do sistema de documentação utilizando MkDocs e o tema Material.
- **Descrição do Projeto**: Documentação detalhada da visão geral, arquitetura, funcionalidades e guia de instalação.
- **Organização**: Separação da documentação em múltiplos módulos para facilitar a leitura.
- **Guia Rápido**: Refatoração do `README.md` para focar em instruções essenciais de execução.
