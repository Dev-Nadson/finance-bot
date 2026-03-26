from sqlalchemy import select
from database.models.db_config import get_session   
from database.models.t01_users import User

async def register_user(user_name: str, telegram_id: int):
    user = User(name=user_name, telegram_id=telegram_id)

    async with get_session() as session:
        user_exists = await session.execute(select(User).filter_by(telegram_id=telegram_id))
        print(user_exists)
        
        if user_exists is None: #essa verificação tá quebrada e o print retorna: <sqlalchemy.engine.result.ChunkedIteratorResult object at 0x71ac03302c50>
            session.add(user)
            return 201
        else:
            return 409 