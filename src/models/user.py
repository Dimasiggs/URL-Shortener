"""Модель пользователя для БД."""
import uuid
from sqlalchemy import UUID, Boolean, DateTime, String, func
from enum import StrEnum
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base_class import Base
from src.schemas.user import UserSchemaBase as UserSchema


class UserRoleEnum(StrEnum):
    """Enum класс со всеми ролями пользователя."""

    ADMIN = "ADMIN"
    USER = "USER"


class User(Base):
    """Модель пользователя для БД."""

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )

    nickname: Mapped[Optional[str]] = mapped_column(
        String(300),
        nullable=False,
        unique=True
    )

    hashed_password: Mapped[Optional[str]] = mapped_column(
        String(300),
        nullable=False
    )

    role: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        default=UserRoleEnum.USER.value
    )

    @property
    def role_enum(self) -> Optional[UserRoleEnum]:
        """Получение роли пользователя, как enum объект для безопасности."""
        if self.role:
            try:
                return UserRoleEnum(self.role)
            except ValueError:
                return None
        return None

    def to_read_model(self) -> UserSchema:
        """Возвращает UserSchema из модели."""
        return UserSchema(
            id=self.id,
            nickname=self.nickname,
        )
