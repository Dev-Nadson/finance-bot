from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes


async def _incomes_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("💰 Registrar Receita", callback_data="inc_add")],
            [InlineKeyboardButton("📋 Ver Receitas", callback_data="inc_list")],
            [InlineKeyboardButton("✏️ Editar Receita", callback_data="inc_edit")],
            [InlineKeyboardButton("🗑️ Excluir Receita", callback_data="inc_delete")],
            [InlineKeyboardButton("🔙 Voltar", callback_data="menu_main")],
        ]
    )
    text = "💰 *Menu de Receitas*\n\nEscolha uma opção:"

    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=keyboard, parse_mode="Markdown")
    else:
        await update.message.reply_text(text, reply_markup=keyboard, parse_mode="Markdown")
