from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from bot.commands import v1

def register_handlers(app: Application):
    app.add_handler(CommandHandler("start",  v1.send_welcome))
    app.add_handler(CommandHandler("chart",  v1.send_chart))
    app.add_handler(CommandHandler("chart2", v1.send_pie_chart))
    # app.add_handler(CommandHandler("menu",   v1.show_menu))
    # app.add_handler(CallbackQueryHandler(v1.handle_callback))
