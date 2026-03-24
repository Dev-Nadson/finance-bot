from telegram.ext import Application, CommandHandler, CallbackQueryHandler
import bot.commands.backend as back
import bot.commands.frontend as front

def register_handlers(app: Application):
    # Frontend
    app.add_handler(CommandHandler("menu",   front.show_menu))
    app.add_handler(CallbackQueryHandler(front.handle_callback))

    # Backend
    app.add_handler(CommandHandler("start",  back.send_welcome))
    app.add_handler(CommandHandler("chart",  back.send_chart))
    app.add_handler(CommandHandler("chart2", back.send_pie_chart))
    
