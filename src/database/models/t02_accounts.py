from sqlalchemy import Column, DateTime, Integer, String, func

from .db_config import Base, engine

class Account(Base):
    __tablename__ = "accounts"
    account_id = Column(Integer, primary_key=True, autoincrement=True)
    # outras colunas
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("\033[32mAccounts table created successfully.\033[0m")  # os números são para deixar verde
