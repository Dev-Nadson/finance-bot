from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from services.repositories.accounts_repository import login_account_repo, list_accounts_repo

LOGIN_NAME, LOGIN_PASS = range(2)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "Operação cancelada."
    if update.callback_query:
        await update.callback_query.edit_message_text(msg)
    else:
        await update.message.reply_text(msg)
    return ConversationHandler.END


async def start_login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "Qual o nome da conta que deseja acessar? (ou /cancelar)"
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(msg)
    else:
        await update.message.reply_text(msg)
    return LOGIN_NAME


async def login_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["login_account_name"] = update.message.text
    await update.message.reply_text("Digite a senha da conta: (ou /cancelar)")
    return LOGIN_PASS


async def login_pass(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = str(update.effective_user.id)
    account_name = context.user_data.pop("login_account_name", "")
    password = update.message.text

    try:
        account, err = await login_account_repo(account_name, password, telegram_id)
        if err:
            await update.message.reply_text(f"❌ Erro: {err}")
        else:
            context.user_data["active_account_id"] = account["id"]
            context.user_data["active_account_name"] = account["name"]
            msg = (
                f"✅ Agora você está na conta *{account['name']}*!\n\n"
                "Todas as despesas, receitas e gráficos usarão esta conta."
            )
            await update.message.reply_text(msg, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"Erro inesperado: {e}")

    return ConversationHandler.END


async def _ensure_active_account(telegram_id: str, context: ContextTypes.DEFAULT_TYPE) -> int | None:
    active_id = context.user_data.get("active_account_id")
    if active_id:
        return active_id

    accounts, _ = await list_accounts_repo(telegram_id)
    if accounts:
        context.user_data["active_account_id"] = accounts[0]["id"]
        context.user_data["active_account_name"] = accounts[0]["name"]
        return accounts[0]["id"]

    return None


def get_login_handler():
    return ConversationHandler(
        entry_points=[
            CallbackQueryHandler(start_login, pattern="^acc_login$"),
            CommandHandler("login_account", start_login),
        ],
        states={
            LOGIN_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, login_name)],
            LOGIN_PASS: [MessageHandler(filters.TEXT & ~filters.COMMAND, login_pass)],
        },
        fallbacks=[CommandHandler("cancelar", cancel)],
    )
