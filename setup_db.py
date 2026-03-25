from src.database.models.db_config import Base, engine
from src.database.models.users import User
from src.database.models.expenses import Expenses

def create_database():
    print('Limpando dados antigos...')

    print('Criando Tabelas...')
    Base.metadata.create_all(bind=engine)
    print("\033[32mSucesso! Tabelas criadas.\033[0m")

if __name__ == '__main__':
    create_database()