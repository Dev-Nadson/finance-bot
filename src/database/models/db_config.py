from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, DateTime, func, Float
from sqlalchemy.orm import declarative_base

from src.config.libs.envroinments import env

engine = create_engine(env.SQL_ALCHEMY_DATABASE_URL)
Base = declarative_base()
