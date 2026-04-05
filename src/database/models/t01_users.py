from sqlalchemy import Column, DateTime, Integer, String, func

from .db_config import Base, engine


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime)

    def to_dict(self):  # me lembra de explicar isso
        return {
            "id": self.user_id,
            "telegram_id": self.telegram_id,
            "name": self.name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("\033[32mUsers table created successfully.\033[0m")  # os números são para deixar verde
