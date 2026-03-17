import bot.app  # noqa: F401
from bot.setup import bot as t_bot

# noqa faz o ruff-fix ignorar a linha acima


def main():
    print("Bot is running 🚀")
    t_bot.polling()


if __name__ == "__main__":
    main()
