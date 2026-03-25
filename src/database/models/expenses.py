from sqlalchemy import create_engine, Column, String, Integer, Float, ForeignKey, DateTime, func
from config.libs.envroinments import env
from sqlalchemy.orm import declarative_base, relationship
from .db_config import Base, engine

class Expenses(Base):
    __tablename__ = "expenses"

    id_expenses = Column(Integer, primary_key = True, unique = True)
    value = Column(Float)
    created_at = Column(DateTime, server_default= func.now())
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("\033[32mExpenses table created successfully.\033[0m")  # os números são para deixar verde