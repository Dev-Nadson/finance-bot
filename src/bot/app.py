from bot.commands import v1
from bot.setup import bot

bot.message_handler(commands=["start"])(v1.send_welcome)
bot.message_handler(commands=["chart"])(v1.send_chart)
bot.message_handler(commands=["chart2"])(v1.send_pie_chart)
bot.message_handler(commands=["menu"])(v1.show_menu)
# @bot.callback_query_handler(func=lambda call: True )
# def callback_query(call):
#     menu.handle_callback(call, bot)
