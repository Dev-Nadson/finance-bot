from src.database.models.db_config import Base, engine


def create_database():
    print("Limpando dados antigos...")

    print("Criando Tabelas...")
    Base.metadata.create_all(bind=engine)
    print("\033[32mSucesso! Tabelas criadas.\033[0m")


if __name__ == "__main__":
    create_database()
