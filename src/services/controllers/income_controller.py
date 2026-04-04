from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from services.repositories.incomes.crud import create_income_repo, list_incomes_repo
from services.repositories.accounts.crud import list_accounts_repo

INC_NAME, INC_VALUE, INC_TYPE, INC_CATEGORY = range(4)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "Operação cancelada."
    if update.callback_query:
         await update.callback_query.edit_message_text(msg)
    else:
         await update.message.reply_text(msg)
    return ConversationHandler.END

async def start_income(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    accs, _ = await list_accounts_repo(user_id)
    if not accs:
        msg = "Você precisa de uma conta antes de registrar receita. (Crie em Contas)"
        if update.callback_query:
            await update.callback_query.edit_message_text(msg)
        else:
            await update.message.reply_text(msg)
        return ConversationHandler.END
        
    account_id = accs[0].get('id')
    context.user_data['account_id'] = account_id

    # Shorthand usage
    if context.args and len(context.args) >= 4:
        name = " ".join(context.args[:-3])
        try:
            value = float(context.args[-3].replace(',', '.'))
        except ValueError:
            await update.message.reply_text("Valor inválido no comando shorthand.")
            return ConversationHandler.END
            
        type_ = context.args[-2]
        category = context.args[-1]
        
        inc, err = await create_income_repo(account_id, value, type_, category, name, user_id)
        if err: await update.message.reply_text(f"Erro: {err}")
        else: await update.message.reply_text(f"Receita '{name}' de R$ {value:.2f} registrada com sucesso!")
        return ConversationHandler.END
        
    msg = "Qual o nome/descrição da sua Receita? (ou /cancelar)"
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(msg)
    else:
        await update.message.reply_text(msg)
    return INC_NAME

async def inc_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['inc_name'] = update.message.text
    await update.message.reply_text("Qual o valor da sua receita? (ex: 2000.00 ou /cancelar)")
    return INC_VALUE

async def inc_value(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.replace(',', '.')
    try:
        val = float(text)
        if val <= 0: raise ValueError
        context.user_data['inc_value'] = val
    except ValueError:
        await update.message.reply_text("Valor inválido. Digite um número positivo.")
        return INC_VALUE
        
    await update.message.reply_text("Qual o tipo da receita? (ex: Pix, Transferência, Boleto)")
    return INC_TYPE

async def inc_type_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['inc_type'] = update.message.text
    await update.message.reply_text("Qual a categoria da receita? (ex: Mensal, Temporário)")
    return INC_CATEGORY

async def inc_category_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    category = update.message.text
    name = context.user_data['inc_name']
    value = context.user_data['inc_value']
    type_ = context.user_data['inc_type']
    account_id = context.user_data['account_id']
    
    inc, err = await create_income_repo(account_id, value, type_, category, name, user_id)
    if err:
        await update.message.reply_text(f"Erro ao registrar receita: {err}")
    else:
        await update.message.reply_text(f"Receita registrada com sucesso! (R$ {value:.2f})")
    
    context.user_data.pop('inc_name', None)
    context.user_data.pop('inc_value', None)
    context.user_data.pop('inc_type', None)
    context.user_data.pop('account_id', None)
    return ConversationHandler.END

def get_income_handler():
    return ConversationHandler(
        entry_points=[
            CallbackQueryHandler(start_income, pattern='^inc_add$'),
            CommandHandler('new_income', start_income),
            CommandHandler('newincome', start_income)
        ],
        states={
            INC_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, inc_name)],
            INC_VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, inc_value)],
            INC_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, inc_type_step)],
            INC_CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, inc_category_step)],
        },
        fallbacks=[CommandHandler('cancelar', cancel)]
    )

async def list_incomes(telegram_id: str):
    return await list_incomes_repo(telegram_id)
