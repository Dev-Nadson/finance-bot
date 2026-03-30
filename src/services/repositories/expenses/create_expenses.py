from sqlalchemy import select
from database.models.db_config import get_session
from database.models.t04_expenses import Expenses

async def creat_expenses_repository(account_id:int, value: float, type: str, category: str, description: str):
    async with get_session() as session:
        expenses = Expenses(account_id = account_id, value = value, type = type, category = category, description = description)
        session.add(expenses)
        return 201