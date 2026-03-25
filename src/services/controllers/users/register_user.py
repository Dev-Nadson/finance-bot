from database.models.db_config import session
from database.models.users import User

async def register_user(user_name: str, telegram_id: int):
    user = User(user_name=user_name, telegram_id=telegram_id)
    session.add(user)
    session.commit()
    print(f"Usuário {user_name} registrado com sucesso!")