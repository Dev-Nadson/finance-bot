import telebot
from telebot import types

from config.libs.enviroinments import env
from services.charts import generate_chart_buffer

bot = telebot.TeleBot(env.TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=["start"])
def send_welcome(msg: types.Message):
    bot.reply_to(msg, "testando")

@bot.message_handler(commands=["chart"])
def send_chart(msg: types.Message):
    chart_file = generate_chart_buffer()
    bot.send_photo(msg.chat.id, chart_file, caption="Aqui está o seu gráfico! 📈")