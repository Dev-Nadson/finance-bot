from sqlalchemy import Column, DateTime, Integer, String, func, ForeignKey, Float, VARCHAR

from .db_config import Base, engine

class Expenses(Base):
    __tablename__ = "expenses"


    expenses_id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('accounts.account_id'), nullable=False)
    value = Column(Float)
    type = Column(VARCHAR)
    category = Column(String)
    description = Column(VARCHAR)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime)
    delete_at = Column(DateTime)


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("\033[32mExpenses table created successfully.\033[0m") 
