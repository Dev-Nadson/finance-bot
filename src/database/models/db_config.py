from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config.libs.envroinments import env

engine = create_engine(env.SQL_ALCHEMY_DATABASE_URL)
_SessionLocal = sessionmaker(engine)
Base = declarative_base()

session = _SessionLocal()