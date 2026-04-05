import asyncio

from database.models.db_config import Base, engine
from database.models.t01_users import User as User
from database.models.t02_accounts import Account as Account
from database.models.t03_users_accounts import UserAccounts as UserAccounts
from database.models.t04_expenses import Expenses as Expenses
from database.models.t05_incomes import Incomes as Incomes


async def create_database():
    async with engine.begin() as conn:
        print("Limpando dados antigos...")
        await conn.run_sync(Base.metadata.drop_all)

        print("Criando Tabelas...")
        await conn.run_sync(Base.metadata.create_all)

    print("\033[32mSucesso! Tabelas criadas.\033[0m")


if __name__ == "__main__":
    asyncio.run(create_database())
