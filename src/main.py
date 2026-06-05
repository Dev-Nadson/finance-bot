import os
import threading

from telegram.ext import Application

from bot.app import register_handlers
from config.libs.envroinments import env
from web.app import app as flask_app


def run_flask():
    flask_app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)


def main():
    app = Application.builder().token(env.TELEGRAM_BOT_TOKEN).build()
    register_handlers(app)

    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    os.system("cls" if os.name == "nt" else "clear")
    print("Bot is running 🚀")
    print("Web dashboard is running on http://127.0.0.1:5000/ 🌐")
    app.run_polling()


if __name__ == "__main__":
    main()
