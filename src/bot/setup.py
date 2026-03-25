# import telebot

# from config.libs.envroinments import env

# bot = telebot.TeleBot(env.TELEGRAM_BOT_TOKEN)
# # explicar problema de importação circular

from config.libs.envroinments import env

TOKEN = env.TELEGRAM_BOT_TOKEN
