from services.repositories.expenses.create_expenses import create_expenses_repository

async def register_user(account_id: int, telegram_id:str, type: str, expenses_name: str, value: float, category: str, description: str):
    code = await create_expenses_repository(
        account_id = account_id,
        telegram_id = telegram_id,
        expenses_name = expenses_name,
        value = value,
        type = type,
        category = category,
        description = description
        )
    return code