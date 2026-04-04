from telegram.ext import Application, CallbackQueryHandler, CommandHandler

import bot.commands.backend as back
import bot.commands.frontend as front
from services.controllers.account_controller import get_account_handler
from services.controllers.expense_controller import get_expense_handler
from services.controllers.income_controller import get_income_handler


def register_handlers(app: Application):
    # Conversations
    app.add_handler(get_account_handler())
    app.add_handler(get_expense_handler())
    app.add_handler(get_income_handler())

    # Frontend
    app.add_handler(CommandHandler("help", front.send_help))
    app.add_handler(CommandHandler("menu", front.show_menu))
    app.add_handler(CallbackQueryHandler(front.handle_callback))
    app.add_handler(CommandHandler("charts", front.charts_menu))
    app.add_handler(CallbackQueryHandler(front.handle_charts_callback))

    # Backend
    app.add_handler(CommandHandler("start", back.send_welcome))
    app.add_handler(CommandHandler("chart", back.send_chart))
    app.add_handler(CommandHandler("chart2", back.send_pie_chart))
