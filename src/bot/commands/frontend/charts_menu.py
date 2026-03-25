from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

async def _charts_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💸 Gráfico de despesas geral", callback_data="expenses_chart")],
        [InlineKeyboardButton("💰 Gráifico de receitas geral", callback_data="incomes_chart")],
        [InlineKeyboardButton("📊 Visualizar evolução de despesas mensal",    callback_data="monthly_expenses_evolution")],
        [InlineKeyboardButton("📊 Visualizar evolução de receita mensal",    callback_data="monthly_incomes_evolution")],
    ])

    if update.callback_query:
        await update.callback_query.edit_message_text("Escolha uma opção:", reply_markup=keyboard)
    else:
        await update.message.reply_text("Escolha uma opção:", reply_markup=keyboard) 
   
async def handle_charts_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    responses = {
        "add_despesa": "Digite o valor da despesa:",
        "add_receita": "Digite o valor da receita:",
        "show_balance": "Consultando saldo...",
        "delete_balance": "Excluindo despesa..."
    }

    await query.message.reply_text(responses.get(query.data, "Opção desconhecida."))