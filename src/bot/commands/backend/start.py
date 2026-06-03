from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from services.controllers.user_controller import register_user
from services.repositories.accounts_repository import list_accounts_repo


async def send_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    telegram_id = update.effective_user.id

    response_code = await register_user(user_name, telegram_id)
    
    accounts, _ = await list_accounts_repo(str(telegram_id))

    if response_code == 409:
        welcome_text = f"Bem-vindo de volta, {user_name}! 👋"
    else:
        welcome_text = f"Olá, {user_name}! 👋 Bem-vindo ao seu *Finance Bot*."

    if not accounts:
        message = (
            f"{welcome_text}\n\n"
            "Parece que você ainda não tem uma conta cadastrada. "
            "Para começar a organizar suas finanças, primeiro crie uma conta bancária."
        )
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Criar Minha Primeira Conta", callback_data="acc_add")]
        ])
    else:
        active_id = context.user_data.get("active_account_id")
        if not active_id:
            # Set first account as default if none active
            context.user_data["active_account_id"] = accounts[0]["id"]
            context.user_data["active_account_name"] = accounts[0]["name"]
            active_id = accounts[0]["id"]

        message = (
            f"{welcome_text}\n\n"
            f"Você está na conta: *{context.user_data['active_account_name']}*.\n"
            "Use o /menu para gerenciar suas receitas e despesas."
        )
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🏠 Abrir Menu Principal", callback_data="menu_main")]
        ])

    await update.message.reply_text(message, parse_mode="Markdown", reply_markup=keyboard)
