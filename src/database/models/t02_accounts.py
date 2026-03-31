from sqlalchemy import Column, DateTime, Integer, String, func, VARCHAR, ForeignKey

from .db_config import Base, engine

class Account(Base):
    __tablename__ = "accounts"
    account_id = Column(Integer,primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    password = Column(VARCHAR, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("\033[32mAccounts table created successfully.\033[0m")  # os números são para deixar verde
