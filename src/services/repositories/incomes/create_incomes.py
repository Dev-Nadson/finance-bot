from sqlalchemy import select
from database.models.db_config import get_session
from database.models.t05_incomes import Incomes

async def creat_incomes_repository(account_id:int, value: float, type: str, category: str, description: str):
    async with get_session() as session:
        incomes = Incomes(account_id = account_id, value = value, type = type, category = category, description = description)
        session.add(incomes)