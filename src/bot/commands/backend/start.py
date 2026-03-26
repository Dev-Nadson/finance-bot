from telegram import Update
from telegram.ext import ContextTypes

from services.controllers.users.register_user import register_user


async def send_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    telegram_id = update.effective_user.id

    response_code = await register_user(user_name, telegram_id)

    if response_code == 409:
        message = "Bem-vindo de volta! Já encontramos seu cadastro."

    if response_code == 201:
        message = f"""
        Olá, {user_name}! 👋 Bem-vindo ao seu *Finance Bot*.\n\n
        Aqui você controla receitas, despesas e acompanha sua saúde financeira — tudo pelo Telegram.\n\n
        Use /menu para acessar as opções principais de forma rápida.
        """

    await update.message.reply_text(message, parse_mode="Markdown")
