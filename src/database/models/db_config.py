from contextlib import asynccontextmanager

from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from config.libs.envroinments import env

engine = create_async_engine(
    env.SQL_ALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # necessário para SQLite em contexto async
)

_SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, autocommit=False, expire_on_commit=False, autoflush=False)
Base = declarative_base()

@asynccontextmanager
async def get_session():
    """
    Uso:
        async with get_session() as session:
            session.add(obj)
    """
    async with _SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise