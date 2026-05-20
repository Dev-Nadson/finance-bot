import asyncio

from src.database.models.db_config import Base, engine
from src.database.models.t01_users import User as User
from src.database.models.t02_accounts import Account as Account
from src.database.models.t03_users_accounts import UserAccounts as UserAccounts
from src.database.models.t04_expenses import Expenses as Expenses
from src.database.models.t05_incomes import Incomes as Incomes


async def create_database():
    async with engine.begin() as conn:
        print("Limpando dados antigos...")
        await conn.run_sync(Base.metadata.drop_all)

        print("Criando Tabelas...")
        await conn.run_sync(Base.metadata.create_all)

    print("\033[32mSucesso! Tabelas criadas.\033[0m")


if __name__ == "__main__":
    asyncio.run(create_database())
