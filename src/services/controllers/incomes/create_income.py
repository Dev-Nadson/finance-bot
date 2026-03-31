from services.repositories.incomes.create_incomes import create_incomes_repository

async def register_income(income_name:str ,value: float, income_type: str, category: str, description: str, account_id: int, telegram_id: str):
    code = await create_incomes_repository(
        account_id=account_id,
        telegram_id=telegram_id,
        name=income_name, 
        value=value, 
        type=income_type, 
        category=category, 
        description=description,
    )
    return code