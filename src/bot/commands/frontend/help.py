from telegram import Update
from telegram.ext import ContextTypes


async def send_help(update: Update, context: ContextTypes.DEFAULT_TYPE):

    help_text = (
        "💸 *Despesas e Receitas*\n"
        "`/new_expense` — registra nova despesa\n"
        "`/new_income` — registra nova receita\n\n"
        "💳 *Contas*\n"
        "`/new_account` — cria uma nova conta\n"
        "`/login_account` — faz login em uma conta existente\n\n"
        "📊 *Gráficos e Resumo*\n"
        "`/saldo` — exibe seu saldo atual\n"
        "`/chart` — gráfico de evolução de saldo/despesas\n"
        "`/chart2` — gráfico de despesas por categoria\n"
        "`/analise` — resumo financeiro inteligente gerado por IA\n\n"
        "⚙️ *Geral*\n"
        "`/start` — inicia o bot\n"
        "`/menu` — exibe o menu principal interativo\n"
        "`/help` — exibe esta mensagem de ajuda\n"
    )

    await update.message.reply_text(help_text, parse_mode="Markdown")
