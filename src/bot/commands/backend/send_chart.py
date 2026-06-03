from telegram import Update
from telegram.ext import ContextTypes

from config.schemas.classes import ChartLinesData
from services.controllers.login_controller import _ensure_active_account
from services.financeiro import monthly_expenses_evolution, monthly_incomes_evolution
from services.reports.charts import generate_lines_chart


async def send_chart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = str(update.effective_user.id)
    account_id = await _ensure_active_account(telegram_id, context)

    if not account_id:
        await update.message.reply_text("Selecione uma conta primeiro com /menu → Contas.")
        return

    exp_labels, exp_totals = await monthly_expenses_evolution(account_id)
    inc_labels, inc_totals = await monthly_incomes_evolution(account_id)

    all_labels = sorted(set(exp_labels) | set(inc_labels))
    if not all_labels:
        await update.message.reply_text("Nenhum dado disponível para gerar o gráfico.")
        return

    exp_by_label = dict(zip(exp_labels, exp_totals))
    inc_by_label = dict(zip(inc_labels, inc_totals))

    y_expenses = [exp_by_label.get(lbl, 0.0) for lbl in all_labels]
    y_incomes = [inc_by_label.get(lbl, 0.0) for lbl in all_labels]

    chart_file = generate_lines_chart(
        ChartLinesData(
            title="Evolução Financeira Mensal",
            x_values=all_labels,
            y_values=[y_expenses, y_incomes],
            xlabel="Mês",
            ylabel="R$",
            series_labels=["Despesas", "Receitas"],
        )
    )
    await update.message.reply_photo(chart_file, caption="📈 Evolução mensal de despesas e receitas")
