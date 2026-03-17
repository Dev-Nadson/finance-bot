from bot.commands import v1
from bot.setup import bot

bot.message_handler(commands=["start"])(v1.send_welcome)
bot.message_handler(commands=["chart"])(v1.send_chart)
