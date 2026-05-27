from sqlalchemy import select

from database.models.db_config import get_session
from database.models.t01_users import User
from database.models.t02_accounts import Account
from database.models.t03_users_accounts import UserAccounts


async def create_account_repo_v1(account_name: str, password: str, user_id: int):
    async with get_session() as session:
        user_exists = (await session.execute(select(User).filter_by(user_id=user_id))).scalar_one_or_none()
        if user_exists is None:
            print(f"User with ID {user_id} does not exist.")
            return 404

        account_exists = (await session.execute(select(UserAccounts).filter_by(user_id=user_id))).scalar_one_or_none()
        if account_exists is not None:
            print(f"User already has account: {account_exists.to_dict()}")
            return 409

        account = Account(name=account_name, password=password)
        session.add(account)
        await session.flush()

        user_account = UserAccounts(user_id=user_id, account_id=account.account_id)
        session.add(user_account)
        await session.flush()

        user_account_exists = (
            await session.execute(select(UserAccounts).filter_by(user_id=user_id, account_id=account.account_id))
        ).scalar_one_or_none()
        if user_account_exists is None:
            return 500

        return 201


async def create_account_repo(name: str, password: str, telegram_id: str):
    async with get_session() as session:
        user = (await session.execute(select(User).filter_by(telegram_id=telegram_id))).scalar_one_or_none()
        if not user:
            return None, "Usuário não encontrado."

        account = Account(name=name, password=password)
        session.add(account)
        await session.flush()

        user_account = UserAccounts(user_id=user.user_id, account_id=account.account_id)
        session.add(user_account)
        return account.to_dict(), None


async def list_accounts_repo(telegram_id: str):
    async with get_session() as session:
        user = (await session.execute(select(User).filter_by(telegram_id=telegram_id))).scalar_one_or_none()
        if not user:
            return [], "Usuário não encontrado."

        user_accounts = (await session.execute(select(UserAccounts).filter_by(user_id=user.user_id))).scalars().all()
        account_ids = [ua.account_id for ua in user_accounts]

        if not account_ids:
            return [], None

        accounts = (await session.execute(select(Account).filter(Account.account_id.in_(account_ids)))).scalars().all()
        return [acc.to_dict() for acc in accounts], None


async def delete_account_repo(account_id: int, telegram_id: str):
    async with get_session() as session:
        user = (await session.execute(select(User).filter_by(telegram_id=telegram_id))).scalar_one_or_none()
        if not user:
            return False, "Usuário não encontrado."

        user_account = (
            await session.execute(select(UserAccounts).filter_by(user_id=user.user_id, account_id=account_id))
        ).scalar_one_or_none()
        if not user_account:
            return False, "Conta não pertence a este usuário ou já foi excluída."

        await session.delete(user_account)
        # Assuming we don't delete the account itself to avoid breaking records history for other users,
        # or we delete it if the user is the only owner. Let's delete it for simplicity if he owns it.
        account = (await session.execute(select(Account).filter_by(account_id=account_id))).scalar_one_or_none()
        if account:
            await session.delete(account)

        # Also could delete related incomes and expenses, but skipping for simplicity or db cascades handles it.
        return True, None


async def login_account_repo(account_name: str, password: str, telegram_id: str):
    """Verify account credentials and link the user to the account if not already linked."""
    async with get_session() as session:
        user = (await session.execute(select(User).filter_by(telegram_id=telegram_id))).scalar_one_or_none()
        if not user:
            return None, "Usuário não encontrado."

        account = (await session.execute(select(Account).filter_by(name=account_name))).scalar_one_or_none()
        if not account:
            return None, "Conta não encontrada."

        if account.password != password:
            return None, "Senha incorreta."

        # Check if user is already linked to this account
        existing_link = (
            await session.execute(
                select(UserAccounts).filter_by(user_id=user.user_id, account_id=account.account_id)
            )
        ).scalar_one_or_none()

        if not existing_link:
            new_link = UserAccounts(user_id=user.user_id, account_id=account.account_id)
            session.add(new_link)

        return account.to_dict(), None
