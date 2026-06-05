# 💸 Finance Bot

**Bot de finanças pessoais para Telegram com suporte a IA, gráficos e controle de contas, receitas e despesas.**

---

## 🌟 Visão Geral

O **Finance Bot** é uma solução moderna para gerenciamento de finanças pessoais diretamente pelo Telegram. Ele combina a simplicidade de uma interface de chat com o poder de análises visuais e inteligência artificial para ajudar usuários a manterem suas contas em dia de forma prática e intuitiva.

Além do bot, o projeto inclui um **Dashboard Web** (Flask) que exibe gráficos interativos e relatórios gerados por IA.

## 🚀 O que você encontrará aqui?

- **[Funcionalidades](features.md)**: Explore tudo o que o bot pode fazer por você.
- **[Instalação e Configuração](setup.md)**: Guia passo a passo para rodar o projeto localmente.
- **[Arquitetura e Estrutura](architecture.md)**: Entenda como o sistema foi construído.
- **[Changelog](changelog.md)**: Acompanhe as últimas atualizações e melhorias.

---

## 🏗️ Objetivo do Projeto

Fornecer uma ferramenta de código aberto que permita a qualquer pessoa ter um controle financeiro rigoroso sem planilhas complexas, utilizando a familiaridade do Telegram e o auxílio de IA para insights inteligentes.

---

## ⚙️ Tecnologias Utilizadas

| Tecnologia | Uso |
|---|---|
| Python 3.12+ | Linguagem principal |
| python-telegram-bot | Framework do bot |
| SQLAlchemy (Async) | ORM para persistência |
| PostgreSQL + asyncpg | Banco de dados |
| Docker / Bitnami | Containerização do banco |
| OpenAI / Groq | IA para relatórios |
| Flask | Dashboard web |
| Matplotlib | Geração de gráficos |
| bcrypt | Hash seguro de senhas |
| uv | Gerenciamento de dependências |
| Ruff | Linting e formatação |