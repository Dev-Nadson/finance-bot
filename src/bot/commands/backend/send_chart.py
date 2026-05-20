from telegram import Update
from telegram.ext import ContextTypes

from config.schemas.classes import ChartLinesData
from services.reports.charts import generate_lines_chart


async def send_chart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chart_file = generate_lines_chart(
        ChartLinesData(
            title="GASTOS POR MÊS",
            x_values=["SEM 1", "SEM 2", "SEM 3", "SEM 4"],
            y_values=[
                [10, 20, 30, 40],
                [15, 25, 35, 45],
                [20, 30, 40, 50],
            ],
            xlabel="Mensal",
            ylabel="Unidades",
            series_labels=["Alimentação", "Lazer", "Necessidades Básicas"],
        )
    )
    await update.message.reply_photo(chart_file, caption="Aqui está o seu gráfico! 📈")
