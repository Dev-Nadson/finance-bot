from sqlalchemy import VARCHAR, Column, DateTime, Float, ForeignKey, Integer, String, func

from .db_config import Base, engine


class Incomes(Base):
    __tablename__ = "incomes"

    incomes_id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey("accounts.account_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    value = Column(Float)
    category = Column(String(255))
    type = Column(VARCHAR)
    description = Column(VARCHAR)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime)
    competencia = Column(String(7), nullable=True)  # formato: "YYYY-MM"
    deleted_at = Column(DateTime)

    def to_dict(self):
        return {
            "incomes_id": self.incomes_id,
            "account_id": self.account_id,
            "user_id": self.user_id,
            "value": self.value,
            "category": self.category,
            "type": self.type,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
            "competencia": self.competencia,
        }


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("\033[32mIncomes table created successfully.\033[0m")
