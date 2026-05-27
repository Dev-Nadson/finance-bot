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
from services.repositories.expenses_repository import (
    create_expense_repo,
    delete_expense_repo,
    list_expenses_repo,
    update_expense_repo,
)

EXPENSE_CATEGORIES = ["Alimentação", "Lazer", "Necessidades Básicas"]

EXP_NAME, EXP_VALUE, EXP_CATEGORY, EXP_EDIT_ID, EXP_EDIT_FIELD, EXP_EDIT_VALUE, EXP_DELETE_ID, EXP_DELETE_CONFIRM = range(8)  # noqa


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "Operação cancelada."
    if update.callback_query:
        await update.callback_query.edit_message_text(msg)
    else:
        await update.message.reply_text(msg)
    return ConversationHandler.END


# ── Create ─────────────────────────────────────────────────────────────────────

async def start_expense(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = str(update.effective_user.id)

    try:
        account_id = await _ensure_active_account(telegram_id, context)
        if not account_id:
            msg = "Você precisa de uma conta antes de registrar despesa. (Crie ou acesse em Contas)"
            if update.callback_query:
                await update.callback_query.edit_message_text(msg)
            else:
                await update.message.reply_text(msg)
            return ConversationHandler.END

        context.user_data["account_id"] = account_id

        msg = "Qual o nome/descrição da sua Despesa? (ou /cancelar)"
        if update.callback_query:
            await update.callback_query.answer()
            await update.callback_query.edit_message_text(msg)
        else:
            await update.message.reply_text(msg)
        return EXP_NAME
    except Exception as e:
        await update.effective_message.reply_text(f"Erro inesperado: {e}")
        return ConversationHandler.END


async def exp_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["exp_name"] = update.message.text
    await update.message.reply_text("Qual o valor da sua despesa? (ex: 150.50 ou /cancelar)")
    return EXP_VALUE


async def exp_value(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.replace(",", ".")
    try:
        val = float(text)
        if val <= 0:
            raise ValueError
        context.user_data["exp_value"] = val
    except ValueError:
        await update.message.reply_text("Valor inválido. Digite um número positivo.")
        return EXP_VALUE

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🍔 Alimentação", callback_data="exp_cat_alimentacao")],
        [InlineKeyboardButton("🎮 Lazer", callback_data="exp_cat_lazer")],
        [InlineKeyboardButton("🏠 Necessidades Básicas", callback_data="exp_cat_necessidades")],
    ])
    await update.message.reply_text("Selecione a categoria da despesa:", reply_markup=keyboard)
    return EXP_CATEGORY


async def exp_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    category_map = {
        "exp_cat_alimentacao": "Alimentação",
        "exp_cat_lazer": "Lazer",
        "exp_cat_necessidades": "Necessidades Básicas",
    }
    category = category_map.get(query.data, "Outros")

    telegram_id = str(update.effective_user.id)
    name = context.user_data["exp_name"]
    value = context.user_data["exp_value"]
    account_id = context.user_data["account_id"]

    try:
        exp, err = await create_expense_repo(account_id, value, category, category, name, telegram_id)
        if err:
            await query.edit_message_text(f"Erro ao registrar despesa: {err}")
        else:
            await query.edit_message_text(
                f"✅ Despesa *{name}* de R$ {value:.2f} ({category}) registrada com sucesso!",
                parse_mode="Markdown",
            )
    except Exception as e:
        await query.edit_message_text(f"Erro inesperado: {e}")

    for key in ("exp_name", "exp_value", "account_id"):
        context.user_data.pop(key, None)
    return ConversationHandler.END


# ── Edit ───────────────────────────────────────────────────────────────────────

async def start_edit_expense(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Digite o ID da despesa que deseja editar: (ou /cancelar)")
    return EXP_EDIT_ID


async def exp_edit_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data["edit_expense_id"] = int(update.message.text.strip())
    except ValueError:
        await update.message.reply_text("ID inválido. Digite apenas o número.")
        return EXP_EDIT_ID

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 Valor", callback_data="exp_edit_value")],
        [InlineKeyboardButton("🍔 Alimentação", callback_data="exp_edit_cat_alimentacao")],
        [InlineKeyboardButton("🎮 Lazer", callback_data="exp_edit_cat_lazer")],
        [InlineKeyboardButton("🏠 Necessidades Básicas", callback_data="exp_edit_cat_necessidades")],
        [InlineKeyboardButton("📝 Descrição", callback_data="exp_edit_description")],
    ])
    await update.message.reply_text("O que deseja editar?", reply_markup=keyboard)
    return EXP_EDIT_FIELD


async def exp_edit_field(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    category_map = {
        "exp_edit_cat_alimentacao": "Alimentação",
        "exp_edit_cat_lazer": "Lazer",
        "exp_edit_cat_necessidades": "Necessidades Básicas",
    }

    if data in category_map:
        # Apply category change directly
        telegram_id = str(update.effective_user.id)
        expense_id = context.user_data.pop("edit_expense_id", None)
        new_category = category_map[data]
        try:
            result, err = await update_expense_repo(expense_id, telegram_id, category=new_category)
            if err:
                await query.edit_message_text(f"Erro: {err}")
            else:
                await query.edit_message_text(f"✅ Categoria atualizada para *{new_category}*!", parse_mode="Markdown")
        except Exception as e:
            await query.edit_message_text(f"Erro inesperado: {e}")
        return ConversationHandler.END

    context.user_data["edit_expense_field"] = data.replace("exp_edit_", "")
    prompts = {
        "value": "Digite o novo valor (ex: 99.90):",
        "description": "Digite a nova descrição:",
    }
    field = data.replace("exp_edit_", "")
    await query.edit_message_text(prompts.get(field, "Digite o novo valor:"))
    return EXP_EDIT_VALUE


async def exp_edit_value(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = str(update.effective_user.id)
    expense_id = context.user_data.pop("edit_expense_id", None)
    field = context.user_data.pop("edit_expense_field", "value")
    raw = update.message.text.strip()

    kwargs = {}
    if field == "value":
        try:
            kwargs["value"] = float(raw.replace(",", "."))
        except ValueError:
            await update.message.reply_text("Valor inválido.")
            return EXP_EDIT_VALUE
    else:
        kwargs["description"] = raw

    try:
        result, err = await update_expense_repo(expense_id, telegram_id, **kwargs)
        if err:
            await update.message.reply_text(f"Erro: {err}")
        else:
            await update.message.reply_text("✅ Despesa atualizada com sucesso!")
    except Exception as e:
        await update.message.reply_text(f"Erro inesperado: {e}")

    return ConversationHandler.END


# ── Delete ─────────────────────────────────────────────────────────────────────

async def start_delete_expense(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Digite o ID da despesa que deseja excluir: (ou /cancelar)")
    return EXP_DELETE_ID


async def exp_delete_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data["delete_expense_id"] = int(update.message.text.strip())
    except ValueError:
        await update.message.reply_text("ID inválido.")
        return EXP_DELETE_ID

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Confirmar exclusão", callback_data="exp_delete_yes"),
            InlineKeyboardButton("❌ Cancelar", callback_data="exp_delete_no"),
        ]
    ])
    await update.message.reply_text(
        f"⚠️ Tem certeza que deseja excluir a despesa #{context.user_data['delete_expense_id']}?",
        reply_markup=keyboard,
    )
    return EXP_DELETE_CONFIRM


async def exp_delete_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "exp_delete_no":
        await query.edit_message_text("Exclusão cancelada.")
        return ConversationHandler.END

    telegram_id = str(update.effective_user.id)
    expense_id = context.user_data.pop("delete_expense_id", None)

    try:
        ok, err = await delete_expense_repo(expense_id, telegram_id)
        if err:
            await query.edit_message_text(f"Erro: {err}")
        else:
            await query.edit_message_text(f"✅ Despesa #{expense_id} excluída com sucesso!")
    except Exception as e:
        await query.edit_message_text(f"Erro inesperado: {e}")

    return ConversationHandler.END


# ── List ───────────────────────────────────────────────────────────────────────

async def list_expenses(telegram_id: str, account_id: int | None = None):
    return await list_expenses_repo(telegram_id, account_id)


# ── Handler ────────────────────────────────────────────────────────────────────

def get_expense_handler():
    return ConversationHandler(
        entry_points=[
            CallbackQueryHandler(start_expense, pattern="^exp_add$"),
            CommandHandler("new_expense", start_expense),
            CallbackQueryHandler(start_edit_expense, pattern="^exp_edit$"),
            CallbackQueryHandler(start_delete_expense, pattern="^exp_delete$"),
        ],
        states={
            EXP_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, exp_name)],
            EXP_VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, exp_value)],
            EXP_CATEGORY: [CallbackQueryHandler(exp_category, pattern="^exp_cat_")],
            EXP_EDIT_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, exp_edit_id)],
            EXP_EDIT_FIELD: [CallbackQueryHandler(exp_edit_field, pattern="^exp_edit_")],
            EXP_EDIT_VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, exp_edit_value)],
            EXP_DELETE_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, exp_delete_id)],
            EXP_DELETE_CONFIRM: [CallbackQueryHandler(exp_delete_confirm, pattern="^exp_delete_")],
        },
        fallbacks=[CommandHandler("cancelar", cancel)],
    )
