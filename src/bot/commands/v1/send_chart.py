from telebot import types

from bot.setup import bot
from services.charts import generate_chart_buffer


def send_chart(msg: types.Message):
    chart_file = generate_chart_buffer()
    bot.send_photo(msg.chat.id, chart_file, caption="Aqui está o seu gráfico! 📈")
