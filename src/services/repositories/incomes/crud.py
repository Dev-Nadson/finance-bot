from sqlalchemy import select, delete
from database.models.db_config import get_session
from database.models.t01_users import User
from database.models.t02_accounts import Account
from database.models.t03_users_accounts import UserAccounts
from database.models.t05_incomes import Incomes

async def create_income_repo(account_id: int, value: float, type: str, category: str, description: str, telegram_id: str):
    async with get_session() as session:
        user = (await session.execute(select(User).filter_by(telegram_id=telegram_id))).scalar_one_or_none()
        if not user:
            return None, "Usuário não encontrado."
            
        account = (await session.execute(select(Account).filter_by(account_id=account_id))).scalar_one_or_none()
        if not account:
            return None, "Conta não encontrada."
            
        user_account = (await session.execute(select(UserAccounts).filter_by(user_id=user.user_id, account_id=account.account_id))).scalar_one_or_none()
        if not user_account:
            return None, "Acesso negado à conta."
            
        income = Incomes(account_id=account_id, user_id=user.user_id, value=value, category=category, type=type, description=description)
        session.add(income)
        await session.flush()
        return income.to_dict(), None

async def list_incomes_repo(telegram_id: str):
    async with get_session() as session:
        user = (await session.execute(select(User).filter_by(telegram_id=telegram_id))).scalar_one_or_none()
        if not user:
            return [], "Usuário não encontrado."
            
        incomes = (await session.execute(select(Incomes).filter_by(user_id=user.user_id))).scalars().all()
        return [inc.to_dict() for inc in incomes], None

async def delete_income_repo(income_id: int, telegram_id: str):
    async with get_session() as session:
        user = (await session.execute(select(User).filter_by(telegram_id=telegram_id))).scalar_one_or_none()
        if not user:
            return False, "Usuário não encontrado."
            
        income = (await session.execute(select(Incomes).filter_by(incomes_id=income_id, user_id=user.user_id))).scalar_one_or_none()
        if not income:
            return False, "Receita não encontrada ou sem permissão."
            
        await session.delete(income)
        return True, None
