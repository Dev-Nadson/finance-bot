from telegram import Update
from telegram.ext import ContextTypes

from config.schemas.classes import ChartPieData
from services.reports.charts import generate_pie_chart


async def send_pie_chart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chart_file = generate_pie_chart(
        ChartPieData(categories=["Alimentação", "Transporte", "Lazer", "Educação"], values=[25, 35, 20, 20])
    )
    await update.message.reply_photo(chart_file, caption="Aqui está o seu gráfico! 📈")
