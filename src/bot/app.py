from bot.setup import bot
from bot.commands import v1

bot.message_handler(commands=["start"])(v1.send_welcome)
bot.message_handler(commands=["chart"])(v1.send_chart)