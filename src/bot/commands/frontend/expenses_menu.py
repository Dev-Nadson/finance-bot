from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

async def _expenses_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💸 Nova despesa", callback_data="add_despesa")],
        [InlineKeyboardButton("💰 Editar despesa", callback_data="add_receita")],
        [InlineKeyboardButton("📊 Visualizar despesas",    callback_data="show_balance")],
        [InlineKeyboardButton("📊 Excluir despesa",    callback_data="delete_balance")],
    ])
    if update.callback_query:
        await update.callback_query.edit_message_text("Escolha uma opção:", reply_markup=keyboard)
    else:
        await update.message.reply_text("Escolha uma opção:", reply_markup=keyboard) 
   
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    responses = {
        "add_despesa": "Digite o valor da despesa:",
        "add_receita": "Digite o valor da receita:",
        "show_balance": "Consultando saldo...",
        "delete_balance": "Excluindo despesa..."
    }

    await query.message.reply_text(responses.get(query.data, "Opção desconhecida."))