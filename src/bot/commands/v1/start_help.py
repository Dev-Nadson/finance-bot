from telebot import types

from bot.setup import bot


def send_welcome(msg: types.Message):
    bot.reply_to(msg, "testando")
