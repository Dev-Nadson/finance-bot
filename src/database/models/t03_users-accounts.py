from sqlalchemy import Column, DateTime, Integer, String, func

from .db_config import Base, engine

class UserAccounts(Base):
    __tablename__ = "users-accounts"
    conection_id = Column(Integer, primary_key=True, autoincrement=True) 
    user_id = Column(String(255), unique=True, nullable=False) # fk user.id
    account_id = Column(String(255), nullable=False) # fk account.id
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("\033[32mUserAccounts table created successfully.\033[0m")  # os números são para deixar verde
