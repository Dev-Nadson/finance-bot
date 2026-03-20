from dataclasses import field

from pydantic import BaseModel


class envConfig(BaseModel):
    SQL_ALCHEMY_DATABASE_URL: str
    TELEGRAM_BOT_TOKEN: str
    GROQ_API_KEY: str
    OPENAI_API_KEY: str


class ChartBaseData(BaseModel):
    xlabel: str = "X"
    ylabel: str = "Y"
    title: str = "Gráfico"


class ChartLinesData(ChartBaseData):
    x_values: list
    y_values: list  # lista simples OU lista de listas múltiplas séries
    series_labels: list[str] = field(default_factory=list)


class ChartPieData(ChartBaseData):
    categories: list[str]
    values: list[float]
