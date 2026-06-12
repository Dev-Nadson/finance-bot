from sqlalchemy import select

from database.models.db_config import get_session
from database.models.t01_users import User
from database.models.t02_accounts import Account
from database.models.t03_users_accounts import UserAccounts
from database.models.t04_expenses import Expenses


async def create_expense_repo(
    account_id: int,
    value: float,
    type: str,
    category: str,
    description: str,
    telegram_id: int | str,
    competencia: str | None = None,
):
    telegram_id = str(telegram_id)
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
            competencia=competencia,
        )
        session.add(expense)
        await session.flush()
        return expense.to_dict(), None


async def list_expenses_repo(
    telegram_id: int | str,
    account_id: int | None = None,
    month: int | None = None,
    year: int | None = None,
):
    telegram_id = str(telegram_id)
    async with get_session() as session:
        user = (await session.execute(select(User).filter_by(telegram_id=telegram_id))).scalar_one_or_none()
        if not user:
            return [], "Usuário não encontrado."

        query = select(Expenses).filter(Expenses.user_id == user.user_id)
        if account_id is not None:
            query = query.filter(Expenses.account_id == account_id)

        if month is not None and year is not None:
            competencia_filter = f"{year:04d}-{month:02d}"
            query = query.filter(Expenses.competencia == competencia_filter)

        expenses = (await session.execute(query)).scalars().all()
        return [ex.to_dict() for ex in expenses], None


async def delete_expense_repo(expense_id: int, telegram_id: int | str):
    telegram_id = str(telegram_id)
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


async def update_expense_repo(
    expense_id: int,
    telegram_id: int | str,
    value: float | None = None,
    category: str | None = None,
    description: str | None = None,
):
    telegram_id = str(telegram_id)
    async with get_session() as session:
        user = (await session.execute(select(User).filter_by(telegram_id=telegram_id))).scalar_one_or_none()
        if not user:
            return None, "Usuário não encontrado."

        expense = (
            await session.execute(select(Expenses).filter_by(expenses_id=expense_id, user_id=user.user_id))
        ).scalar_one_or_none()
        if not expense:
            return None, "Despesa não encontrada ou sem permissão."

        if value is not None:
            expense.value = value
        if category is not None:
            expense.category = category
        if description is not None:
            expense.description = description

        return expense.to_dict(), None
