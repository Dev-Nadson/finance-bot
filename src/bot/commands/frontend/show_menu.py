from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from services.controllers.balance import calculate_balance

from .accounts_menu import _accounts_menu
from .expenses_menu import _expenses_menu
from .incomes_menu import _incomes_menu


async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _show_main_menu(update, context)


async def _show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("💳 Contas", callback_data="menu_contas")],
            [InlineKeyboardButton("💰 Receitas", callback_data="menu_receitas")],
            [InlineKeyboardButton("💸 Despesas", callback_data="menu_despesas")],
            [InlineKeyboardButton("📊 Saldo Geral", callback_data="show_balance")],
        ]
    )
    text = "Escolha uma opção do menu principal:"

    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=keyboard)
    else:
        await update.message.reply_text(text, reply_markup=keyboard)


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    # Main menu routing
    if data == "menu_main":
        await _show_main_menu(update, context)
    elif data == "menu_contas":
        await _accounts_menu(update, context)
    elif data == "menu_receitas":
        await _incomes_menu(update, context)
    elif data == "menu_despesas":
        await _expenses_menu(update, context)
    elif data == "show_balance":
        user_id = str(update.effective_user.id)
        incomes, expenses, balance, err = await calculate_balance(user_id)
        if err:
            text = f"Erro ao calcular saldo:\n{err}"
        else:
            text = f"📊 *SALDO GERAL*\n\n💰 Receitas: R$ {incomes:.2f}\n💸 Despesas: R$ {expenses:.2f}\n⚖️ Saldo: R$ {balance:.2f}" # noqa E501

        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Voltar", callback_data="menu_main")]])
        await query.edit_message_text(text, reply_markup=keyboard, parse_mode="Markdown")

    # Accounts Menu Handlers
    elif data.startswith("acc_"):
        await _handle_accounts(update, context, data)
    # Incomes Menu Handlers
    elif data.startswith("inc_"):
        await _handle_incomes(update, context, data)
    # Expenses Menu Handlers
    elif data.startswith("exp_"):
        await _handle_expenses(update, context, data)
    else:
        await query.message.reply_text("Opção desconhecida ou em desenvolvimento.")


async def _handle_accounts(update, context, data):
    from services.controllers.account_controller import list_accounts

    query = update.callback_query
    user_id = str(update.effective_user.id)
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Voltar", callback_data="menu_contas")]])

    if data == "acc_list":
        accs, err = await list_accounts(user_id)
        if err:
            await query.edit_message_text(f"Erro: {err}", reply_markup=keyboard)
        else:
            if not accs:
                await query.edit_message_text("Nenhuma conta encontrada.", reply_markup=keyboard)
            else:
                text = "💳 *Suas Contas:*\n\n"
                for a in accs:
                    text += f"Nome: {a.get('name')} (ID: {a.get('id')})\n"
                await query.edit_message_text(text, reply_markup=keyboard, parse_mode="Markdown")


async def _handle_incomes(update, context, data):
    from services.controllers.income_controller import list_incomes

    query = update.callback_query
    user_id = str(update.effective_user.id)
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Voltar", callback_data="menu_receitas")]])

    if data == "inc_list":
        incs, err = await list_incomes(user_id)
        if err:
            await query.edit_message_text(f"Erro: {err}", reply_markup=keyboard)
        else:
            if not incs:
                await query.edit_message_text("Nenhuma receita.", reply_markup=keyboard)
            else:
                text = "💰 *Suas Receitas:*\n\n"
                for i in incs:
                    text += f"R$ {i.get('value')} - {i.get('description')} (Cat: {i.get('category')})\n"
                await query.edit_message_text(text, reply_markup=keyboard, parse_mode="Markdown")


async def _handle_expenses(update, context, data):
    from services.controllers.expense_controller import list_expenses

    query = update.callback_query
    user_id = str(update.effective_user.id)
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Voltar", callback_data="menu_despesas")]])

    if data == "exp_list":
        exps, err = await list_expenses(user_id)
        if err:
            await query.edit_message_text(f"Erro: {err}", reply_markup=keyboard)
        else:
            if not exps:
                await query.edit_message_text("Nenhuma despesa.", reply_markup=keyboard)
            else:
                text = "💸 *Suas Despesas:*\n\n"
                for i in exps:
                    text += f"R$ {i.get('value')} - {i.get('description')} (Cat: {i.get('category')})\n"
                await query.edit_message_text(text, reply_markup=keyboard, parse_mode="Markdown")
