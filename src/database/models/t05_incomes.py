from sqlalchemy import Column, DateTime, Integer, String, func, ForeignKey,Float,VARCHAR

from .db_config import Base, engine

class Incomes(Base):
    __tablename__ = "incomes"

    incomes_id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('accounts.account_id'), nullable=False)
    value = Column(Float)   
    category = Column(String(255))
    type = Column(VARCHAR)
    description = Column(VARCHAR)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(  ))
    deleted_at = Column(DateTime, server_default=func.now())

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("\033[32mIncomes table created successfully.\033[0m")  # os números são para deixar verde
