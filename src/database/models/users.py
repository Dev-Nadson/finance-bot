from sqlalchemy import Column, DateTime, Integer, String, create_engine, func
from sqlalchemy.orm import relationship

from config.libs.envroinments import env

from .db_config import Base

engine = create_engine(env.SQL_ALCHEMY_DATABASE_URL)


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    expenses = relationship("Expenses", back_populates="user")
    incomes = relationship("Incomes", back_populates="user")


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("\033[32mUsers table created successfully.\033[0m")  # os números são para deixar verde
