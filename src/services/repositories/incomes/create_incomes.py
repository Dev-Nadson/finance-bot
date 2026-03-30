from sqlalchemy import select
from database.models.db_config import get_session
from database.models.t01_users import User
from database.models.t02_accounts import Account
from database.models.t05_incomes import Incomes

async def create_incomes_repository(incomes_id:int, value: float, type: str, category: str, description: str,account_id: int, telegram_id: str):
    async with get_session() as session:
        account_exists = (await session.execute(select(Account).filter_by(account_id=account_id))).scalar_one_or_none()
        user_exists = (await session.execute(select(User).filter_by(telegram_id=telegram_id))).scalar_one_or_none()

        if account_exists is None:
            print(f'Erro: Conta não encontrada')
            return 404
        if user_exists is None:
            print(f'Usuario não encontrado') 
            return 404
        if account_exists.user_id != user_exists.user_id:
            print(f'Segurança: Usuário {telegram_id} tentou acessar conta de terceiros')
            return 403
        
        incomes = Incomes(account_id = account_id, value = value, category = category, type = type, description = description)
        session.add(incomes)
        return 201