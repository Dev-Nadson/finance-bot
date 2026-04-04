from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from services.repositories.expenses.crud import create_expense_repo, list_expenses_repo
from services.repositories.accounts.crud import list_accounts_repo

EXP_NAME, EXP_VALUE, EXP_TYPE, EXP_CATEGORY = range(4)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "Operação cancelada."
    if update.callback_query:
         await update.callback_query.edit_message_text(msg)
    else:
         await update.message.reply_text(msg)
    return ConversationHandler.END

async def start_expense(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    accs, _ = await list_accounts_repo(user_id)
    if not accs:
        msg = "Você precisa de uma conta antes de registrar despesa. (Crie em Contas)"
        if update.callback_query:
            await update.callback_query.edit_message_text(msg)
        else:
            await update.message.reply_text(msg)
        return ConversationHandler.END
        
    account_id = accs[0].get('id')
    context.user_data['account_id'] = account_id

    # Shorthand usage: /new-expense {nome} {100} {Alimentação} {Mensal}
    if context.args and len(context.args) >= 4:
        # Simplistic split, last 3 are value type category
        name = " ".join(context.args[:-3])
        try:
            value = float(context.args[-3].replace(',', '.'))
        except ValueError:
            await update.message.reply_text("Valor inválido no comando shorthand.")
            return ConversationHandler.END
            
        type_ = context.args[-2]
        category = context.args[-1]
        
        exp, err = await create_expense_repo(account_id, value, type_, category, name, user_id)
        if err: await update.message.reply_text(f"Erro: {err}")
        else: await update.message.reply_text(f"Despesa '{name}' de R$ {value:.2f} registrada com sucesso!")
        return ConversationHandler.END
        
    msg = "Qual o nome/descrição da sua Despesa? (ou /cancelar)"
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(msg)
    else:
        await update.message.reply_text(msg)
    return EXP_NAME

async def exp_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['exp_name'] = update.message.text
    await update.message.reply_text("Qual o valor da sua despesa? (ex: 150.50 ou /cancelar)")
    return EXP_VALUE

async def exp_value(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.replace(',', '.')
    try:
        val = float(text)
        if val <= 0: raise ValueError
        context.user_data['exp_value'] = val
    except ValueError:
        await update.message.reply_text("Valor inválido. Digite um número positivo.")
        return EXP_VALUE
        
    await update.message.reply_text("Qual o tipo da despesa? (ex: Alimentação, Casa, Transporte)")
    return EXP_TYPE

async def exp_type_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['exp_type'] = update.message.text
    await update.message.reply_text("Qual a categoria da despesa? (ex: Mensal, Único, Semanal)")
    return EXP_CATEGORY

async def exp_category_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    category = update.message.text
    name = context.user_data['exp_name']
    value = context.user_data['exp_value']
    type_ = context.user_data['exp_type']
    account_id = context.user_data['account_id']
    
    exp, err = await create_expense_repo(account_id, value, type_, category, name, user_id)
    if err:
        await update.message.reply_text(f"Erro ao registrar despesa: {err}")
    else:
        await update.message.reply_text(f"Despesa registrada com sucesso! (R$ {value:.2f})")
    
    context.user_data.pop('exp_name', None)
    context.user_data.pop('exp_value', None)
    context.user_data.pop('exp_type', None)
    context.user_data.pop('account_id', None)
    return ConversationHandler.END

def get_expense_handler():
    return ConversationHandler(
        entry_points=[
            CallbackQueryHandler(start_expense, pattern='^exp_add$'),
            CommandHandler('new_expense', start_expense),
            CommandHandler('newexpense', start_expense)
        ],
        states={
            EXP_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, exp_name)],
            EXP_VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, exp_value)],
            EXP_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, exp_type_step)],
            EXP_CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, exp_category_step)],
        },
        fallbacks=[CommandHandler('cancelar', cancel)]
    )

async def list_expenses(telegram_id: str):
    return await list_expenses_repo(telegram_id)
