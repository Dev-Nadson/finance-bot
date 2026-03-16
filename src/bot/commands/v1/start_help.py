from bot.setup import bot
from telebot import types

def send_welcome(msg: types.Message):
    bot.reply_to(msg, "testando")