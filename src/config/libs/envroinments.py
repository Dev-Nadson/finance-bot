import os

from dotenv import load_dotenv
from config.models.classes import envConfig

load_dotenv()

env = envConfig(
    TELEGRAM_BOT_TOKEN=os.getenv("TELEGRAM_BOT_TOKEN"),
    GROQ_API_KEY=os.getenv("GROQ_API_KEY"),
    OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
)
