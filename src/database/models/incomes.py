from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, func

from .db_config import Base, engine


class Incomes(Base):
    __tablename__ = "incomes"

    id_incomes = Column(Integer, primary_key=True, unique=True)
    value = Column(Float)
    created_at = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("\033[32mIncomes table created successfully.\033[0m")  # os números são para deixar verde
