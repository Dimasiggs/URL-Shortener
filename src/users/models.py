"""Модель пользователя для БД."""

from sqlalchemy import UUID, String
from enum import StrEnum
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
import uuid

from src.database import Base
from src.users.schemas import UserSchemaBase


class UserRoleEnum(StrEnum):
    """Enum класс со всеми ролями пользователя."""

    ADMIN = "ADMIN"
    USER = "USER"


class User(Base):
    """Модель пользователя для БД."""

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    nickname: Mapped[Optional[str]] = mapped_column(
        String(300), nullable=False, unique=True
    )

    hashed_password: Mapped[Optional[str]] = mapped_column(String(300), nullable=False)

    role: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, default=UserRoleEnum.USER.value
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

    def to_read_model(self) -> UserSchemaBase:
        """Возвращает UserSchema из модели."""
        return UserSchemaBase(
            id=self.id,
            nickname=self.nickname,
        )
