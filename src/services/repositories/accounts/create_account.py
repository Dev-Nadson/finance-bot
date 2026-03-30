from sqlalchemy import select
from database.models.db_config import get_session   
from database.models.t01_users import User
from database.models.t02_accounts import Account
from database.models.t03_users_accounts import UserAccounts


async def create_account_repository(account_name: str, user_id: int):
    async with get_session() as session:
        user_exists = (await session.execute(select(User).filter_by(user_id=user_id))).scalar_one_or_none()
        if user_exists is None:
            print(f"User with ID {user_id} does not exist.") #dev
            return 404

        account_exists = (await session.execute(select(UserAccounts).filter_by(user_id=user_id))).scalar_one_or_none()
        if account_exists is not None: 
            print(account_exists.to_dict()) #dev
            return 409
        
        account = Account(name=account_name, user_id=user_id)
        session.add(account)
        await session.flush()
    
        user_account = UserAccounts(user_id=user_id, account_id=account.account_id)
        session.add(user_account)
        await session.flush()
    
        user_account_exists = (await session.execute(select(UserAccounts).filter_by(user_id=user_id, account_id=account.account_id))).scalar_one_or_none()
        if user_account_exists is not None: 
            print(user_account_exists.to_dict()) #dev
            return 500

        return 201 # user_account_exists.todict()