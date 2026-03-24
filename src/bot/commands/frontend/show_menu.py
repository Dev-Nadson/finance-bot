from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from .expenses_menu import _expenses_menu

async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💸 Registrar Despesa", callback_data="add_despesa")],
        [InlineKeyboardButton("💰 Registrar Receita", callback_data="add_receita")],
        [InlineKeyboardButton("📊 Calcular Saldo",    callback_data="show_balance")],
    ])
    await update.message.reply_text("Escolha uma opção:", reply_markup=keyboard)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "add_despesa":
        await _expenses_menu(update, context)
    if query.data == "add_receita":
        await query.message.reply_text("Digite o valor da receita:")
    elif query.data == "show_balance":
        await query.message.reply_text("Consultando saldo...")
    else:
        await query.message.reply_text("Opção desconhecida.")