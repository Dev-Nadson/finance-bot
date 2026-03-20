from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

from src.config.libs.envroinments import env

engine = create_engine(env.SQL_ALCHEMY_DATABASE_URL)
Base = declarative_base()
