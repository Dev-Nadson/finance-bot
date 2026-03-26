from sqlalchemy import select
from database.models.db_config import get_session   
from database.models.t01_users import User

async def create_user_repository(user_name: str, telegram_id: str):
    user = User(name=user_name, telegram_id=telegram_id)

    async with get_session() as session:
        user_exists = (await session.execute(select(User).filter_by(telegram_id=telegram_id))).scalar_one_or_none()

        if user_exists is not None: 
            print(user_exists.to_dict()) #dev
            return 409 
        else:
            session.add(user)
            return 201