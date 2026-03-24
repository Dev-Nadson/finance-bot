from config.schemas.classes import ChartLinesData
from services.reports.charts import generate_lines_chart

from telegram import Update
from telegram.ext import ContextTypes

async def send_chart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chart_file = generate_lines_chart(
        ChartLinesData(
            title="Vendas por Canal — 2024",
            x_values=["Q1", "Q2", "Q3", "Q4"],
            y_values=[
                [120, 145, 162, 190],
                [80, 95, 110, 140],
                [55, 70, 88, 105],
            ],
            xlabel="Trimestre",
            ylabel="Unidades",
            series_labels=["Online", "Loja Física", "Parceiros"],
        )
    )
    await update.message.reply_photo(chart_file, caption="Aqui está o seu gráfico! 📈")
