from bot.commands import v1
from bot.setup import bot

bot.message_handler(commands=["start"])(v1.send_welcome)
bot.message_handler(commands=["chart"])(v1.send_chart)
<<<<<<< HEAD
bot.message_handler(commands=["menu"])(lambda msg: menu.show_menu(msg, bot))
bot.callback_query_handler(func=lambda call: True )
    def callback_query(call): 
        menu.handle_callback(call, bot)
=======
>>>>>>> 110644d7bc063693772c2f4c75ec0e8718bdea9f
