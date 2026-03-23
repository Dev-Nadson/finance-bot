from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from bot.commands.backend import v1
import bot.commands.frontend as front

def register_handlers(app: Application):
    # Frontend
    app.add_handler(CommandHandler("menu",   front.show_menu))
    app.add_handler(CallbackQueryHandler(front.handle_callback))

    # Backend
    app.add_handler(CommandHandler("start",  v1.send_welcome))
    app.add_handler(CommandHandler("chart",  v1.send_chart))
    app.add_handler(CommandHandler("chart2", v1.send_pie_chart))
    
