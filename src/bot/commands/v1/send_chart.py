from telebot import types

from bot.setup import bot
from services.reports.charts import generate_lines_chart
from config.schemas.classes import ChartLinesData

def send_chart(msg: types.Message):
    chart_file = generate_lines_chart(ChartLinesData(x_values=[3, 13, 27, 32, 42], y_values=[71, 17, 40, 33, 66]))
    bot.send_photo(msg.chat.id, chart_file, caption="Aqui está o seu gráfico! 📈")
