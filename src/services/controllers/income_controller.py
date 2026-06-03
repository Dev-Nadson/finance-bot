from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from services.controllers.login_controller import _ensure_active_account
from services.repositories.incomes_repository import (
    create_income_repo,
    delete_income_repo,
    list_incomes_repo,
    update_income_repo,
)

INC_NAME, INC_VALUE, INC_TYPE, INC_EDIT_ID, INC_EDIT_FIELD, INC_EDIT_VALUE, INC_DELETE_ID, INC_DELETE_CONFIRM = range(8)  # noqa


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "Operação cancelada."
    if update.callback_query:
        await update.callback_query.edit_message_text(msg)
    else:
        await update.message.reply_text(msg)
    return ConversationHandler.END


async def start_income(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = str(update.effective_user.id)
    try:
        account_id = await _ensure_active_account(telegram_id, context)
        if not account_id:
            msg = "Você precisa de uma conta antes de registrar receita. (Crie ou acesse em Contas)"
            if update.callback_query:
                await update.callback_query.edit_message_text(msg)
            else:
                await update.message.reply_text(msg)
            return ConversationHandler.END

        context.user_data["account_id"] = account_id

        msg = "Qual o nome/descrição da sua Receita? (ou /cancelar)"
        if update.callback_query:
            await update.callback_query.answer()
            await update.callback_query.edit_message_text(msg)
        else:
            await update.message.reply_text(msg)
        return INC_NAME
    except Exception as e:
        await update.effective_message.reply_text(f"Erro inesperado: {e}")
        return ConversationHandler.END


async def inc_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["inc_name"] = update.message.text
    await update.message.reply_text("Qual o valor da sua receita? (ex: 2000.00 ou /cancelar)")
    return INC_VALUE


async def inc_value(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.replace(",", ".")
    try:
        val = float(text)
        if val <= 0:
            raise ValueError
        context.user_data["inc_value"] = val
    except ValueError:
        await update.message.reply_text("Valor inválido. Digite um número positivo.")
        return INC_VALUE

    await update.message.reply_text("Qual o tipo da receita? (ex: Pix, Transferência, Boleto ou /cancelar)")
    return INC_TYPE


async def inc_type_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = str(update.effective_user.id)
    inc_type = update.message.text
    name = context.user_data["inc_name"]
    value = context.user_data["inc_value"]
    account_id = context.user_data["account_id"]

    try:
        inc, err = await create_income_repo(account_id, value, inc_type, inc_type, name, telegram_id)
        if err:
            await update.message.reply_text(f"Erro ao registrar receita: {err}")
        else:
            from telegram import InlineKeyboardButton, InlineKeyboardMarkup
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("💰 Mais Receitas", callback_data="menu_receitas"),
                 InlineKeyboardButton("🏠 Menu", callback_data="menu_main")]
            ])
            await update.message.reply_text(
                f"✅ Receita *{name}* de R$ {value:.2f} registrada!",
                parse_mode="Markdown",
                reply_markup=keyboard
            )
    except Exception as e:
        await update.message.reply_text(f"Erro inesperado: {e}")

    for key in ("inc_name", "inc_value", "account_id"):
        context.user_data.pop(key, None)
    return ConversationHandler.END


async def start_edit_income(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Digite o ID da receita que deseja editar: (ou /cancelar)")
    return INC_EDIT_ID


async def inc_edit_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data["edit_income_id"] = int(update.message.text.strip())
    except ValueError:
        await update.message.reply_text("ID inválido.")
        return INC_EDIT_ID

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 Valor", callback_data="inc_edit_value")],
        [InlineKeyboardButton("📝 Descrição", callback_data="inc_edit_description")],
    ])
    await update.message.reply_text("O que deseja editar?", reply_markup=keyboard)
    return INC_EDIT_FIELD


async def inc_edit_field(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    field = query.data.replace("inc_edit_", "")
    context.user_data["edit_income_field"] = field
    prompts = {"value": "Digite o novo valor (ex: 2000.00):", "description": "Digite a nova descrição:"}
    await query.edit_message_text(prompts.get(field, "Digite o novo valor:"))
    return INC_EDIT_VALUE


async def inc_edit_value(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = str(update.effective_user.id)
    income_id = context.user_data.pop("edit_income_id", None)
    field = context.user_data.pop("edit_income_field", "value")
    raw = update.message.text.strip()

    kwargs = {}
    if field == "value":
        try:
            kwargs["value"] = float(raw.replace(",", "."))
        except ValueError:
            await update.message.reply_text("Valor inválido.")
            return INC_EDIT_VALUE
    else:
        kwargs["description"] = raw

    try:
        result, err = await update_income_repo(income_id, telegram_id, **kwargs)
        if err:
            await update.message.reply_text(f"Erro: {err}")
        else:
            await update.message.reply_text("✅ Receita atualizada com sucesso!")
    except Exception as e:
        await update.message.reply_text(f"Erro inesperado: {e}")
    return ConversationHandler.END


async def start_delete_income(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Digite o ID da receita que deseja excluir: (ou /cancelar)")
    return INC_DELETE_ID


async def inc_delete_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data["delete_income_id"] = int(update.message.text.strip())
    except ValueError:
        await update.message.reply_text("ID inválido.")
        return INC_DELETE_ID

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Confirmar", callback_data="inc_delete_yes"),
            InlineKeyboardButton("❌ Cancelar", callback_data="inc_delete_no"),
        ]
    ])
    await update.message.reply_text(
        f"⚠️ Tem certeza que deseja excluir a receita #{context.user_data['delete_income_id']}?",
        reply_markup=keyboard,
    )
    return INC_DELETE_CONFIRM


async def inc_delete_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "inc_delete_no":
        await query.edit_message_text("Exclusão cancelada.")
        return ConversationHandler.END

    telegram_id = str(update.effective_user.id)
    income_id = context.user_data.pop("delete_income_id", None)

    try:
        ok, err = await delete_income_repo(income_id, telegram_id)
        if err:
            await query.edit_message_text(f"Erro: {err}")
        else:
            await query.edit_message_text(f"✅ Receita #{income_id} excluída com sucesso!")
    except Exception as e:
        await query.edit_message_text(f"Erro inesperado: {e}")
    return ConversationHandler.END


async def list_incomes(telegram_id: str, account_id: int | None = None):
    return await list_incomes_repo(telegram_id, account_id)


def get_income_handler():
    return ConversationHandler(
        entry_points=[
            CallbackQueryHandler(start_income, pattern="^inc_add$"),
            CommandHandler("new_income", start_income),
            CallbackQueryHandler(start_edit_income, pattern="^inc_edit$"),
            CallbackQueryHandler(start_delete_income, pattern="^inc_delete$"),
        ],
        states={
            INC_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, inc_name)],
            INC_VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, inc_value)],
            INC_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, inc_type_step)],
            INC_EDIT_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, inc_edit_id)],
            INC_EDIT_FIELD: [CallbackQueryHandler(inc_edit_field, pattern="^inc_edit_")],
            INC_EDIT_VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, inc_edit_value)],
            INC_DELETE_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, inc_delete_id)],
            INC_DELETE_CONFIRM: [CallbackQueryHandler(inc_delete_confirm, pattern="^inc_delete_")],
        },
        fallbacks=[CommandHandler("cancelar", cancel)],
    )
