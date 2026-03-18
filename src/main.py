import os

import bot.app  # noqa: F401
from bot.setup import bot as t_bot

# noqa faz o ruff-fix ignorar a linha acima


def main():
    os.system("cls" if os.name == "nt" else "clear")
    print("Bot is running 🚀")
    t_bot.polling()


if __name__ == "__main__":
    main()
