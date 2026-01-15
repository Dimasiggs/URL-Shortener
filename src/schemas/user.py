"""Схемы для пользователя."""

from uuid import UUID
from pydantic import BaseModel
from pydantic.config import ConfigDict


class UserSchemaBase(BaseModel):
    """Базовая схема для пользователей, от которой наследуется большинство схем."""

    id: UUID
    email: str

    model_config = ConfigDict(from_attributes=True)


class UserSchemaAdd(BaseModel):
    """Схема для добавления пользователей."""

    email: str
    hashed_password: str
