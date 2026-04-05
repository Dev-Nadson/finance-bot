from services.repositories.accounts.crud import create_account_repo, list_accounts_repo
from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

ACCOUNT_NAME, ACCOUNT_PASS = range(2)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "Operação cancelada."
    if update.callback_query:
        await update.callback_query.edit_message_text(msg)
    else:
        await update.message.reply_text(msg)
    return ConversationHandler.END


async def start_account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Shorthand check
    if context.args and len(context.args) >= 2:
        name = context.args[0]
        password = " ".join(context.args[1:])
        user_id = str(update.effective_user.id)

        acc, err = await create_account_repo(name, password, user_id)
        msg_text = f"Erro: {err}" if err else f"Conta '{acc['name']}' criada com sucesso!"
        await update.message.reply_text(msg_text)
        return ConversationHandler.END

    msg = "Qual o nome da sua Conta bancária? (ou /cancelar)"
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(msg)
    else:
        await update.message.reply_text(msg)
    return ACCOUNT_NAME


async def account_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["account_name"] = update.message.text
    await update.message.reply_text("Escolha uma senha para essa conta: (ou /cancelar)")
    return ACCOUNT_PASS


async def account_pass(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = context.user_data["account_name"]
    password = update.message.text
    user_id = str(update.effective_user.id)

    acc, err = await create_account_repo(name, password, user_id)
    if err:
        await update.message.reply_text(f"Erro ao criar conta: {err}")
    else:
        await update.message.reply_text(f"Conta '{acc['name']}' criada com sucesso!")

    context.user_data.pop("account_name", None)
    return ConversationHandler.END


def get_account_handler():
    return ConversationHandler(
        entry_points=[
            CallbackQueryHandler(start_account, pattern="^acc_add$"),
            CommandHandler("new_account", start_account),
        ],
        states={
            ACCOUNT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, account_name)],
            ACCOUNT_PASS: [MessageHandler(filters.TEXT & ~filters.COMMAND, account_pass)],
        },
        fallbacks=[CommandHandler("cancelar", cancel)],
    )


async def list_accounts(telegram_id: str):
    return await list_accounts_repo(telegram_id)
