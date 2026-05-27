from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes


async def _expenses_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("💸 Nova Despesa", callback_data="exp_add")],
            [InlineKeyboardButton("📋 Ver Despesas", callback_data="exp_list")],
            [InlineKeyboardButton("✏️ Editar Despesa", callback_data="exp_edit")],
            [InlineKeyboardButton("🗑️ Excluir Despesa", callback_data="exp_delete")],
            [InlineKeyboardButton("🔙 Voltar", callback_data="menu_main")],
        ]
    )
    text = "💸 *Menu de Despesas*\n\nEscolha uma opção:"
    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=keyboard, parse_mode="Markdown")
    else:
        await update.message.reply_text(text, reply_markup=keyboard, parse_mode="Markdown")
