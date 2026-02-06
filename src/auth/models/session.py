"""Модель сессий пользователей для БД."""

from sqlalchemy import UUID
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
import uuid

from src.database import Base
from src.users.schemas import UserSchemaBase



class Session(Base):
    """Модель токенов сессий для БД."""

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False
    )

    # TODO: Доделать
    expires_data: Mapped[datetime] = mapped_column(
        default=None,

    )

    

    def to_read_model(self) -> UserSchemaBase:
        """Возвращает UserSchema из модели."""
        return UserSchemaBase(
            id=self.id,
            nickname=self.nickname,
        )
