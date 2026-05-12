# 💸 Finance Bot

**Bot de finanças pessoais para Telegram com suporte a IA, gráficos e controle de contas, receitas e despesas.**

---

## 🚀 Guia Rápido

Para começar a usar o bot localmente, siga os passos abaixo:

### 1. Instalação
Certifique-se de ter o [uv](https://docs.astral.sh/uv/) instalado.
```bash
uv sync
```

### 2. Configuração
```bash
cp .env.example .env
# Edite o arquivo .env com seu TELEGRAM_BOT_TOKEN e chaves de API (Groq/OpenAI)
```

### 3. Banco de Dados
```bash
uv run setup_db.py
```

### 4. Execução
```bash
uv run src/main.py
```

---

## 📖 Documentação Completa

Para informações detalhadas sobre a arquitetura, estrutura de pastas, guia completo de instalação e tecnologias utilizadas, consulte nossa documentação oficial:

👉 **[Documentação Completa (Docs)](docs/index.md)**

*(Ou execute `uv run mkdocs serve` para visualizar a documentação em formato web)*
