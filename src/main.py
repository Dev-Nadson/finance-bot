import os

from telegram.ext import Application

from bot.app import register_handlers
from config.libs.envroinments import env


def main():
    app = Application.builder().token(env.TELEGRAM_BOT_TOKEN).build()
    register_handlers(app)

    os.system("cls" if os.name == "nt" else "clear")
    print("Bot is running 🚀")
    app.run_polling()


if __name__ == "__main__":
    main()
