from telegram import Update
from telegram.ext import ContextTypes


async def send_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nome = update.effective_user.first_name

    texto = (
        f"Olá, {nome}! 👋 Bem-vindo ao seu *Finance Bot*.\n\n"
        "Aqui você controla receitas, despesas e acompanha sua saúde financeira — tudo pelo Telegram.\n\n"
        "💸 *Despesas*\n"
        "`/despesa` — lista todas as despesas\n"
        "`/despesa-new <valor> <categoria>` — registra nova despesa\n"
        "`/despesa-edit <id> <campo> <valor>` — edita uma despesa\n"
        "`/despesa-remove <id>` — remove uma despesa\n\n"
        "💰 *Receitas*\n"
        "`/receita` — lista todas as receitas\n"
        "`/receita-new <valor> <categoria>` — registra nova receita\n"
        "`/receita-edit <id> <campo> <valor>` — edita uma receita\n"
        "`/receita-remove <id>` — remove uma receita\n\n"
        "📊 *Gráficos e resumo*\n"
        "`/saldo` — exibe seu saldo atual\n"
        "`/geral` — gráfico geral de finanças\n"
        "`/geral-despesa` — gráfico por categoria de despesa\n"
        "`/geral-receita` — gráfico por categoria de receita\n"
        "`/resumo` — resumo financeiro gerado por IA\n\n"
        "Use /menu para acessar as opções principais de forma rápida."
    )

    await update.message.reply_text(texto, parse_mode="Markdown")
