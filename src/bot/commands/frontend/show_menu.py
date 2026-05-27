from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from services.controllers.balance import calculate_balance
from services.controllers.login_controller import _ensure_active_account

from .accounts_menu import _accounts_menu
from .expenses_menu import _expenses_menu
from .incomes_menu import _incomes_menu


async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _show_main_menu(update, context)


async def _show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    active_name = context.user_data.get("active_account_name", "Nenhuma")
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("💳 Contas", callback_data="menu_contas")],
            [InlineKeyboardButton("💰 Receitas", callback_data="menu_receitas")],
            [InlineKeyboardButton("💸 Despesas", callback_data="menu_despesas")],
            [InlineKeyboardButton("📊 Saldo Geral", callback_data="show_balance")],
            [InlineKeyboardButton("📈 Gráficos", callback_data="menu_charts")],
        ]
    )
    text = f"🏠 *Menu Principal*\n\n🔵 Conta ativa: *{active_name}*\n\nEscolha uma opção:"

    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=keyboard, parse_mode="Markdown")
    else:
        await update.message.reply_text(text, reply_markup=keyboard, parse_mode="Markdown")


async def _charts_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🥧 Despesas por Categoria", callback_data="chart_pie_expenses")],
            [InlineKeyboardButton("📈 Evolução de Despesas", callback_data="chart_line_expenses")],
            [InlineKeyboardButton("📈 Evolução de Receitas", callback_data="chart_line_incomes")],
            [InlineKeyboardButton("🔙 Voltar", callback_data="menu_main")],
        ]
    )
    chart_text = "📊 *Gráficos*\n\nEscolha o gráfico:"
    if update.callback_query:
        await update.callback_query.edit_message_text(chart_text, reply_markup=keyboard, parse_mode="Markdown")
    else:
        await update.message.reply_text(chart_text, reply_markup=keyboard, parse_mode="Markdown")


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "menu_main":
        await _show_main_menu(update, context)
    elif data == "menu_contas":
        await _accounts_menu(update, context)
    elif data == "menu_receitas":
        await _incomes_menu(update, context)
    elif data == "menu_despesas":
        await _expenses_menu(update, context)
    elif data == "menu_charts":
        await _charts_menu(update, context)
    elif data == "show_balance":
        telegram_id = str(update.effective_user.id)
        incomes, expenses, balance, err = await calculate_balance(telegram_id, context)
        active_name = context.user_data.get("active_account_name", "Ativa")
        if err:
            text = f"Erro ao calcular saldo:\n{err}"
        else:
            text = (
                f"📊 *SALDO GERAL — {active_name}*\n\n"
                f"💰 Receitas: R$ {incomes:.2f}\n"
                f"💸 Despesas: R$ {expenses:.2f}\n"
                f"⚖️ Saldo: R$ {balance:.2f}"
            )
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Voltar", callback_data="menu_main")]])
        await query.edit_message_text(text, reply_markup=keyboard, parse_mode="Markdown")

    elif data.startswith("acc_"):
        await _handle_accounts(update, context, data)
    elif data.startswith("inc_"):
        await _handle_incomes(update, context, data)
    elif data.startswith("exp_"):
        await _handle_expenses(update, context, data)
    elif data.startswith("chart_"):
        await _handle_charts(update, context, data)
    else:
        await query.message.reply_text("Opção desconhecida ou em desenvolvimento.")


async def _handle_accounts(update, context, data):
    from services.controllers.account_controller import list_accounts
    from services.controllers.login_controller import get_login_handler  # noqa — imported for side effect

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
                active_id = context.user_data.get("active_account_id")
                text = "💳 *Suas Contas:*\n\n"
                for a in accs:
                    marker = " 🔵" if a.get("id") == active_id else ""
                    text += f"• *{a.get('name')}* (ID: {a.get('id')}){marker}\n"
                await query.edit_message_text(text, reply_markup=keyboard, parse_mode="Markdown")

    elif data == "acc_switch":
        accs, err = await list_accounts(user_id)
        if err or not accs:
            await query.edit_message_text("Nenhuma conta disponível.", reply_markup=keyboard)
        else:
            buttons = [
                [InlineKeyboardButton(f"• {a['name']}", callback_data=f"acc_select_{a['id']}")]
                for a in accs
            ]
            buttons.append([InlineKeyboardButton("🔙 Voltar", callback_data="menu_contas")])
            await query.edit_message_text(
                "Selecione a conta que deseja ativar:",
                reply_markup=InlineKeyboardMarkup(buttons),
            )

    elif data.startswith("acc_select_"):
        account_id = int(data.replace("acc_select_", ""))
        accs, _ = await list_accounts(user_id)
        selected = next((a for a in accs if a["id"] == account_id), None)
        if selected:
            context.user_data["active_account_id"] = selected["id"]
            context.user_data["active_account_name"] = selected["name"]
            await query.edit_message_text(
                f"✅ Conta *{selected['name']}* ativada!", parse_mode="Markdown", reply_markup=keyboard
            )
        else:
            await query.edit_message_text("Conta não encontrada.", reply_markup=keyboard)


async def _handle_incomes(update, context, data):
    from services.controllers.income_controller import list_incomes

    query = update.callback_query
    user_id = str(update.effective_user.id)
    account_id = context.user_data.get("active_account_id")
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Voltar", callback_data="menu_receitas")]])

    if data == "inc_list":
        incs, err = await list_incomes(user_id, account_id)
        if err:
            await query.edit_message_text(f"Erro: {err}", reply_markup=keyboard)
        elif not incs:
            await query.edit_message_text("Nenhuma receita registrada.", reply_markup=keyboard)
        else:
            text = "💰 *Suas Receitas:*\n\n"
            for i in incs:
                text += f"• #{i.get('incomes_id')} R$ {i.get('value'):.2f} — {i.get('description')} ({i.get('type')})\n"
            await query.edit_message_text(text, reply_markup=keyboard, parse_mode="Markdown")


async def _handle_expenses(update, context, data):
    from services.controllers.expense_controller import list_expenses

    query = update.callback_query
    user_id = str(update.effective_user.id)
    account_id = context.user_data.get("active_account_id")
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Voltar", callback_data="menu_despesas")]])

    if data == "exp_list":
        exps, err = await list_expenses(user_id, account_id)
        if err:
            await query.edit_message_text(f"Erro: {err}", reply_markup=keyboard)
        elif not exps:
            await query.edit_message_text("Nenhuma despesa registrada.", reply_markup=keyboard)
        else:
            text = "💸 *Suas Despesas:*\n\n"
            for e in exps:
                exp_id = e.get('expenses_id')
                val = e.get('value', 0)
                desc = e.get('description')
                cat = e.get('category')
                text += f"• #{exp_id} R$ {val:.2f} — {desc} [{cat}]\n"
            await query.edit_message_text(text, reply_markup=keyboard, parse_mode="Markdown")


async def _handle_charts(update, context, data):
    from services.financeiro import (
        total_expenses_by_category,
        monthly_expenses_evolution,
        monthly_incomes_evolution,
    )
    from services.reports.charts import generate_pie_chart, generate_lines_chart
    from config.schemas.classes import ChartPieData, ChartLinesData

    query = update.callback_query
    user_id = str(update.effective_user.id)
    account_id = await _ensure_active_account(user_id, context)

    if not account_id:
        await query.message.reply_text("Selecione uma conta primeiro em 💳 Contas.")
        return

    if data == "chart_pie_expenses":
        await query.message.reply_text("⏳ Gerando gráfico de despesas...")
        category_data = await total_expenses_by_category(account_id)
        if not category_data:
            await query.message.reply_text("Nenhuma despesa registrada nesta conta.")
            return
        chart = generate_pie_chart(
            ChartPieData(
                title="Despesas por Categoria",
                categories=list(category_data.keys()),
                values=list(category_data.values()),
            )
        )
        await query.message.reply_photo(chart, caption="🥧 Despesas por categoria")

    elif data == "chart_line_expenses":
        await query.message.reply_text("⏳ Gerando gráfico de evolução de despesas...")
        labels, totals = await monthly_expenses_evolution(account_id)
        if not labels:
            await query.message.reply_text("Nenhum dado de despesa disponível.")
            return
        chart = generate_lines_chart(
            ChartLinesData(
                title="Evolução de Despesas",
                x_values=labels,
                y_values=totals,
                xlabel="Mês",
                ylabel="R$",
            )
        )
        await query.message.reply_photo(chart, caption="📈 Evolução mensal de despesas")

    elif data == "chart_line_incomes":
        await query.message.reply_text("⏳ Gerando gráfico de evolução de receitas...")
        labels, totals = await monthly_incomes_evolution(account_id)
        if not labels:
            await query.message.reply_text("Nenhum dado de receita disponível.")
            return
        chart = generate_lines_chart(
            ChartLinesData(
                title="Evolução de Receitas",
                x_values=labels,
                y_values=totals,
                xlabel="Mês",
                ylabel="R$",
            )
        )
        await query.message.reply_photo(chart, caption="📈 Evolução mensal de receitas")
