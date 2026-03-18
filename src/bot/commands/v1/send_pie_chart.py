from telebot import types
from bot.setup import bot
from services.reports.charts import generate_pie_chart
from config.schemas.classes import ChartPieData

def send_pie_chart(msg: types.Message):
    chart_file = generate_pie_chart(ChartPieData(categories=["Alimentação", "Transporte", "Lazer", "Educação"], values=[25, 35, 20, 20]))
    bot.send_photo(msg.chat.id, chart_file, caption="Aqui está o seu gráfico! 📈")
