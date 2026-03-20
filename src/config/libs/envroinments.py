import os

from dotenv import load_dotenv

from config.schemas.classes import envConfig

load_dotenv()

env = envConfig(
    SQL_ALCHEMY_DATABASE_URL=os.getenv("SQL_ALCHEMY_DATABASE_URL"),
    TELEGRAM_BOT_TOKEN=os.getenv("TELEGRAM_BOT_TOKEN"),
    GROQ_API_KEY=os.getenv("GROQ_API_KEY"),
    OPENAI_API_KEY=os.getenv("OPENAI_API_KEY"),
)
