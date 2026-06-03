from sqlalchemy import VARCHAR, Column, DateTime, Integer, String, func

from .db_config import Base, engine


class Account(Base):
    __tablename__ = "accounts"
    account_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    password = Column(VARCHAR, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())

    def to_dict(self):
        return {
            "id": self.account_id,
            "name": self.name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "password": self.password,
        }


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("\033[32mAccounts table created successfully.\033[0m")
