from sqlalchemy import select
from database.models.db_config import get_session   
from database.models.t02_accounts import Account

async def create_account_repository(account_name: str, user_id: int):
    # Verificar se o usuário existe
    # Verificar se a conta já existe para o usuário
    # Se não existir, criar a conta e associar ao usuário
    # pensar se ele cria a conta manuakmente ou se é criado automaticamente quando o usuário é criado

    account = Account(name=account_name, user_id=user_id)

    async with get_session() as session:
        pass
        # account_exists = (await session.execute(select(Account).filter_by(name=account_name, user_id=user_id))).scalar_one_or_none()

        # if account_exists is not None: 
        #     print(account_exists.to_dict()) #dev
        #     return 409 
        # else:
        #     session.add(account)
        #     return 201