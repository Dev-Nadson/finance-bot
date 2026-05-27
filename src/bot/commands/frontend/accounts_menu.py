from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes


async def _accounts_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    active_name = context.user_data.get("active_account_name", "Nenhuma")

    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("➕ Criar Conta", callback_data="acc_add")],
            [InlineKeyboardButton("🔐 Entrar em uma Conta", callback_data="acc_login")],
            [InlineKeyboardButton("🔄 Trocar de Conta", callback_data="acc_switch")],
            [InlineKeyboardButton("📋 Minhas Contas", callback_data="acc_list")],
            [InlineKeyboardButton("🔙 Voltar", callback_data="menu_main")],
        ]
    )
    text = f"💳 *Menu de Contas*\n\n🔵 Conta ativa: *{active_name}*\n\nEscolha uma opção:"

    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=keyboard, parse_mode="Markdown")
    else:
        await update.message.reply_text(text, reply_markup=keyboard, parse_mode="Markdown")
