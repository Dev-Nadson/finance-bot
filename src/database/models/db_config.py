from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config.libs.envroinments import env

engine = create_engine(
    env.SQL_ALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # necessário para SQLite em contexto async
)

_SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


@contextmanager
def get_session():
    """
    Uso:
        with get_session() as session:
            session.add(obj)
    """
    session = _SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()