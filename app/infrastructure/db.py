from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import db_settings


class Base(DeclarativeBase):
    pass


engine = create_async_engine(
    db_settings.DATABASE_URL,
    echo=db_settings.DEBUG,
    pool_pre_ping=True,
    autocommit=False,
    autoflush=False,
    future=True
)


AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
    future=True
)

