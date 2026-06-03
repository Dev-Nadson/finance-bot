from telegram import Update
from telegram.ext import ContextTypes

from services.controllers.login_controller import _ensure_active_account
from services.financeiro import calculate_balance


async def send_saldo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = str(update.effective_user.id)
    account_id = await _ensure_active_account(telegram_id, context)
    if not account_id:
        await update.message.reply_text("Selecione uma conta primeiro com /menu → Contas.")
        return

    incomes, expenses, balance, err = await calculate_balance(account_id)
    if err:
        await update.message.reply_text(f"Erro ao calcular saldo: {err}")
        return

    active_name = context.user_data.get("active_account_name", "Conta Ativa")
    text = (
        f"📊 *SALDO GERAL — {active_name}*\n\n"
        f"💰 Receitas totais: R$ {incomes:.2f}\n"
        f"💸 Despesas totais: R$ {expenses:.2f}\n"
        f"⚖️ Saldo: R$ {balance:.2f}"
    )
    await update.message.reply_text(text, parse_mode="Markdown")
