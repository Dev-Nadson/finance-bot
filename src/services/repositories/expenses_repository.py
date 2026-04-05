from sqlalchemy import select

from database.models.db_config import get_session
from database.models.t01_users import User
from database.models.t02_accounts import Account
from database.models.t03_users_accounts import UserAccounts
from database.models.t04_expenses import Expenses


async def create_expenses_repository(
    account_id: int, value: float, type: str, category: str, description: str, telegram_id: str
):
    async with get_session() as session:
        account_exists = (await session.execute(select(Account).filter_by(account_id=account_id))).scalar_one_or_none()
        user_exists = (await session.execute(select(User).filter_by(telegram_id=telegram_id))).scalar_one_or_none()

        if account_exists is None:
            print("Erro: Conta não encontrada")  # to_dict
            return 404
        if user_exists is None:
            print("Usuario não encontrado")  # to_dict
            return 404
        if account_exists.user_id != user_exists.user_id:  # verifica se a conta é do usuario
            print(f"Segurança: Usuário {telegram_id} tentou acessar conta de terceiros")
            return 403

        expenses = Expenses(account_id=account_id, value=value, type=type, category=category, description=description)
        session.add(expenses)
        await session.commit()
        return 201


async def create_expense_repo(
    account_id: int, value: float, type: str, category: str, description: str, telegram_id: str
):
    async with get_session() as session:
        user = (await session.execute(select(User).filter_by(telegram_id=telegram_id))).scalar_one_or_none()
        if not user:
            return None, "Usuário não encontrado."

        account = (await session.execute(select(Account).filter_by(account_id=account_id))).scalar_one_or_none()
        if not account:
            return None, "Conta não encontrada."

        user_account = (
            await session.execute(select(UserAccounts).filter_by(user_id=user.user_id, account_id=account.account_id))
        ).scalar_one_or_none()
        if not user_account:
            return None, "Acesso negado à conta."

        expense = Expenses(
            account_id=account_id,
            user_id=user.user_id,
            value=value,
            type=type,
            category=category,
            description=description,
        )
        session.add(expense)
        await session.flush()
        return expense.to_dict(), None


async def list_expenses_repo(telegram_id: str):
    async with get_session() as session:
        user = (await session.execute(select(User).filter_by(telegram_id=telegram_id))).scalar_one_or_none()
        if not user:
            return [], "Usuário não encontrado."

        expenses = (await session.execute(select(Expenses).filter_by(user_id=user.user_id))).scalars().all()
        return [ex.to_dict() for ex in expenses], None


async def delete_expense_repo(expense_id: int, telegram_id: str):
    async with get_session() as session:
        user = (await session.execute(select(User).filter_by(telegram_id=telegram_id))).scalar_one_or_none()
        if not user:
            return False, "Usuário não encontrado."

        expense = (
            await session.execute(select(Expenses).filter_by(expenses_id=expense_id, user_id=user.user_id))
        ).scalar_one_or_none()
        if not expense:
            return False, "Despesa não encontrada ou sem permissão."

        await session.delete(expense)
        return True, None
