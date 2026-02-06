"""Настройка подключения к базе данных и базовый класс для моделей БД."""

from collections.abc import AsyncIterator
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase

from src.config import settings

from contextlib import asynccontextmanager

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    pool_size=5,
    max_overflow=10,
)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    """Базовый класс для всех моделей БД."""

    @declared_attr
    def __tablename__(cls) -> str:
        """Генерирует __tablename__ автоматически из имени класса."""
        return cls.__name__.lower()


@asynccontextmanager
async def get_async_connection() -> AsyncIterator[AsyncSession]:
    """Возвращает async context manager для сессии."""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# Для FastAPI Depends (без context manager):
async def get_session() -> AsyncIterator[AsyncSession]:
    """Возвращает асинхронную сессиию."""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
