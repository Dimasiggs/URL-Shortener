"""Настройка подключения к базе данных и базовый класс для моделей БД."""

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase

from src.core.config import settings

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


async def get_async_session():
    """Возвращает асинхронную сессию БД."""
    async with async_session_maker() as session:
        yield session
