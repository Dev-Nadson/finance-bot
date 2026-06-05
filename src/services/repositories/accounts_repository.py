import bcrypt
from sqlalchemy import select

from database.models.db_config import get_session
from database.models.t01_users import User
from database.models.t02_accounts import Account
from database.models.t03_users_accounts import UserAccounts


async def create_account_repo(name: str, password: str, telegram_id: int | str):
    telegram_id = str(telegram_id)
    async with get_session() as session:
        user = (await session.execute(select(User).filter_by(telegram_id=telegram_id))).scalar_one_or_none()
        if not user:
            return None, "Usuário não encontrado."

        # Verificar unicidade global do nome (necessário pois o login busca por nome)
        existing = (await session.execute(select(Account).filter_by(name=name))).scalar_one_or_none()
        if existing:
            return None, f"Já existe uma conta com o nome '{name}'. Escolha um nome diferente."

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        account = Account(name=name, password=hashed_password)
        session.add(account)
        await session.flush()

        user_account = UserAccounts(user_id=user.user_id, account_id=account.account_id)
        session.add(user_account)
        return account.to_dict(), None


async def list_accounts_repo(telegram_id: int | str):
    telegram_id = str(telegram_id)
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


async def login_account_repo(account_name: str, password: str, telegram_id: int | str):
    """Verify account credentials and link the user to the account if not already linked."""
    telegram_id = str(telegram_id)
    async with get_session() as session:
        user = (await session.execute(select(User).filter_by(telegram_id=telegram_id))).scalar_one_or_none()
        if not user:
            return None, "Usuário não encontrado."

        account = (await session.execute(select(Account).filter_by(name=account_name))).scalar_one_or_none()
        if not account:
            return None, "Conta não encontrada."

        if not bcrypt.checkpw(password.encode('utf-8'), account.password.encode('utf-8')):
            return None, "Senha incorreta."

        existing_link = (
            await session.execute(
                select(UserAccounts).filter_by(user_id=user.user_id, account_id=account.account_id)
            )
        ).scalar_one_or_none()

        if not existing_link:
            new_link = UserAccounts(user_id=user.user_id, account_id=account.account_id)
            session.add(new_link)

        return account.to_dict(), None
