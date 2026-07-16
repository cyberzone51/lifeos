"""Database session — async SQLAlchemy engine and session factory."""

import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# Use SQLite for testing if no DATABASE_URL or if it's PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", settings.DATABASE_URL)

# For testing, use SQLite
if "sqlite" in DATABASE_URL or not DATABASE_URL.startswith("postgresql"):
    DATABASE_URL = "sqlite+aiosqlite:///./lifeos_test.db"
    connect_args = {"check_same_thread": False}
else:
    connect_args = {}

engine = create_async_engine(
    DATABASE_URL,
    echo=settings.DEBUG,
    connect_args=connect_args,
)

async_session_factory = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def init_db():
    """Create all tables for testing."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
