"""Модель пользователя для БД."""
import uuid
from sqlalchemy import UUID, String
from enum import StrEnum
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base_class import Base
from src.schemas.user import UserSchemaBase as UserSchema


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

    

    def to_read_model(self) -> UserSchema:
        """Возвращает UserSchema из модели."""
        return UserSchema(
            id=self.id,
            nickname=self.nickname,
        )
