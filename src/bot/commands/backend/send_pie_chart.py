from telegram import Update
from telegram.ext import ContextTypes

from config.schemas.classes import ChartPieData
from services.controllers.login_controller import _ensure_active_account
from services.financeiro import total_expenses_by_category
from services.reports.charts import generate_pie_chart


async def send_pie_chart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = str(update.effective_user.id)
    account_id = await _ensure_active_account(telegram_id, context)

    if not account_id:
        await update.message.reply_text("Selecione uma conta primeiro com /menu → Contas.")
        return

    category_data = await total_expenses_by_category(account_id)

    if not category_data:
        await update.message.reply_text("Nenhuma despesa registrada nesta conta.")
        return

    chart_file = generate_pie_chart(
        ChartPieData(
            title="Despesas por Categoria",
            categories=list(category_data.keys()),
            values=list(category_data.values()),
        )
    )
    await update.message.reply_photo(chart_file, caption="🥧 Despesas por categoria")
