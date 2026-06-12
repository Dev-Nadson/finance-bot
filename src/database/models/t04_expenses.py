from sqlalchemy import VARCHAR, Column, DateTime, Float, ForeignKey, Integer, String, func

from .db_config import Base, engine


class Expenses(Base):
    __tablename__ = "expenses"

    expenses_id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey("accounts.account_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    value = Column(Float)
    type = Column(VARCHAR)
    category = Column(String)
    description = Column(VARCHAR)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime)
    delete_at = Column(DateTime)
    competencia = Column(String(7), nullable=True)  

    def to_dict(self):
        return {
            "expenses_id": self.expenses_id,
            "account_id": self.account_id,
            "user_id": self.user_id,
            "value": self.value,
            "type": self.type,
            "category": self.category,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.delete_at,
            "competencia": self.competencia,
        }


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("\033[32mExpenses table created successfully.\033[0m")
