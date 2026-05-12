# 🏗️ Arquitetura e Estrutura

O **Finance Bot** foi projetado com foco em modularidade e separação de responsabilidades, facilitando a expansão de funcionalidades e a manutenção do código.

## Padrões de Projeto

O sistema segue uma arquitetura em camadas:

- **Interface (Bot)**: Implementada na pasta `src/bot/`, lida exclusivamente com a API do Telegram e o registro de comandos.
- **Controladores (Business Logic)**: Localizados em `src/services/controllers/`, gerenciam o fluxo de conversas (ConversationHandler) e a lógica de decisão.
- **Repositórios (Data Access)**: Abstraem as consultas ao banco de dados em `src/services/repositories/`.
- **Modelos (Database)**: Definem a estrutura das tabelas em `src/database/models/` utilizando SQLAlchemy.
- **Configuração**: Centralizada em `src/config/` para lidar com variáveis de ambiente e clientes de terceiros de forma segura e validada.

## Estrutura de Pastas

```text
finance-bot/
├── docs/                               # Documentação do projeto (MkDocs)
├── src/
│   ├── main.py                         # Ponto de entrada da aplicação
│   ├── bot/
│   │   ├── app.py                      # Registro de todos os handlers
│   │   └── commands/                   # Lógica dos comandos (frontend/backend)
│   ├── config/
│   │   ├── libs/                       # Clientes de APIs (Groq, OpenAI)
│   │   └── schemas/                    # Validação de dados com Pydantic
│   ├── database/
│   │   ├── models/                     # Definição de tabelas SQLAlchemy
│   │   └── connection.py               # Gerenciamento de sessões async
│   └── services/
│       ├── controllers/                # Lógica de negócio e diálogos do bot
│       ├── repositories/               # Camada de persistência
│       └── reports/                    # Geração de gráficos e relatórios
├── pyproject.toml                      # Configuração do projeto e dependências
└── README.md                           # Guia rápido para novos desenvolvedores
```

## Tecnologias

- **Linguagem**: Python 3.12+
- **Bot Framework**: `python-telegram-bot`
- **Banco de Dados**: SQLite (com suporte planejado para PostgreSQL)
- **ORM**: `SQLAlchemy` (Async)
- **IA**: APIs da `Groq` e `OpenAI`
- **Gerenciamento**: `uv`
