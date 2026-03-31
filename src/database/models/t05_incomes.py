from sqlalchemy import Column, DateTime, Integer, String, func, ForeignKey,Float,VARCHAR

from .db_config import Base, engine

class Incomes(Base):
    __tablename__ = "incomes"

    incomes_id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('accounts.account_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable = False)
    name = Column(String(255), nullable=False)
    value = Column(Float)   
    category = Column(String(255))
    type = Column(VARCHAR)
    description = Column(VARCHAR)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)

    def to_dict(self):
            return {
             'incomes_id': self.incomes_id,
             'account_id': self.account_id,
             'user_id': self.user_id,
             'value': self.value,
             'category': self.category,
             'type': self.type,
             'description': self.description,
             'created_at': self.created_at,
             'updated_at': self.updated_at,
             'deleted_at': self.delete_at
            }


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("\033[32mIncomes table created successfully.\033[0m")  # os números são para deixar verde
