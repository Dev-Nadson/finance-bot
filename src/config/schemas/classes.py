from pydantic import BaseModel


class envConfig(BaseModel):
    TELEGRAM_BOT_TOKEN: str
    GROQ_API_KEY: str
    OPENAI_API_KEY: str
