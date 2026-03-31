from sqlalchemy import select
from database.models.db_config import get_session
from database.models.t01_users import User
from database.models.t02_accounts import Account
from database.models.t04_expenses import Expenses

async def create_expenses_repository(account_id:int, value: float, type: str, category: str, description: str, telegram_id: str):
    async with get_session() as session:
        account_exists = (await session.execute(select(Account).filter_by(account_id=account_id))).scalar_one_or_none()
        user_exists = (await session.execute(select(User).filter_by(telegram_id=telegram_id))).scalar_one_or_none()

        if account_exists is None:
            print(f'Erro: Conta não encontrada') # to_dict
            return 404
        if user_exists is None:
            print(f'Usuario não encontrado') # to_dict
            return 404
        if account_exists.user_id != user_exists.user_id: # verifica se a conta é do usuario
            print(f'Segurança: Usuário {telegram_id} tentou acessar conta de terceiros')
            return 403
        
        try:
            expenses = Expenses(account_id = account_id, value = value, type = type, category = category, description = description)
            session.add(expenses)
            await session.commit()
            return 201
        except Exception as e:
            await session.rollback()
            print(f'Erro Critico no banco: {e}')
            return 500