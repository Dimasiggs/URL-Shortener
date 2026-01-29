"""Схемы для пользователя."""

from uuid import UUID
from pydantic import BaseModel
from pydantic.config import ConfigDict


class UserSchemaBase(BaseModel):
    """Базовая схема для пользователей, от которой наследуется большинство схем."""

    id: UUID

    model_config = ConfigDict(from_attributes=True)


class UserSchemaAdd(BaseModel):
    """Схема для добавления пользователей."""

    nickname: str
    hashed_password: str


# TODO: Rename
class UserRegisterRequest(BaseModel):
    """Схема для запроса на добавление пользователей."""
    
    nickname: str
    password: str


class UserRegisterResponse(BaseModel):
    """Схема для ответа на запрос на добавление пользователей."""
    token: str
    refresh_token: str
