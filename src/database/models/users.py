from sqlalchemy import Column, Integer, String

from .db_config import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)


if __name__ == "__main__":
    from .db_config import engine

    Base.metadata.create_all(bind=engine)
    print("\033[32mUsers table created successfully.\033[0m")  # os números são para deixar verde
