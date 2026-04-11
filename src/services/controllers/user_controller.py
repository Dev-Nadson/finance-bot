from services.repositories.user_repository import create_user_repository


async def register_user(user_name: str, telegram_id: int):
    code = await create_user_repository(user_name=user_name, telegram_id=telegram_id)
    return code
