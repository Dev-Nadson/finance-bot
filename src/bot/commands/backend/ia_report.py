from datetime import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from services.controllers.ai_controller import generate_financial_report
from services.controllers.login_controller import _ensure_active_account


async def send_ai_analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Command /analise to generate AI financial insights."""
    telegram_id = str(update.effective_user.id)
    account_id = await _ensure_active_account(telegram_id, context)

    if not account_id:
        await update.message.reply_text("Selecione uma conta primeiro em /menu → 💳 Contas.")
        return

    await update.message.reply_text("⏳ Analisando seus dados financeiros com IA... Aguarde um momento.")

    now = datetime.now()
    month = context.user_data.get("active_month", now.month)
    year = context.user_data.get("active_year", now.year)

    try:
        text = await generate_financial_report(telegram_id, account_id, month, year)
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Menu Principal", callback_data="menu_main")]])
        await update.message.reply_text(text, parse_mode="HTML", reply_markup=keyboard)
    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao gerar análise: {e}")
