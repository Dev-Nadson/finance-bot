from sqlalchemy import Column, DateTime, Integer, String, func, ForeignKey

from .db_config import Base, engine

class UserAccounts(Base):
    __tablename__ = "users-accounts"
    user_acc_id = Column(Integer, primary_key=True, autoincrement=True) 
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    account_id = Column(Integer, ForeignKey('accounts.account_id'),nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime)

    def to_dict(self):
        return {
            "user_acc_id": self.user_acc_id,
            'user_id': self.user_id,
            'account_id': self.account_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("\033[32mUserAccounts table created successfully.\033[0m")
