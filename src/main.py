import os

from telegram.ext import Application
from bot.app import register_handlers
from bot.setup import TOKEN

def main():
    app = Application.builder().token(TOKEN).build()
    register_handlers(app)

    os.system("cls" if os.name == "nt" else "clear")
    print("Bot is running 🚀")
    app.run_polling()  #async

if __name__ == "__main__":
    main()