"""Схемы для пользователя."""

from uuid import UUID
from pydantic import BaseModel
from pydantic.config import ConfigDict


class UserSchemaBase(BaseModel):
    """Базовая схема для пользователей, от которой наследуется большинство схем."""

    id: UUID
    model_config = ConfigDict(from_attributes=True)


class UserSchemaFull(UserSchemaBase):
    """Полная схема пользователя"""
    nickname: str
    hashed_password: str
    salt: str
    role: str


class UserSchemaAdd(BaseModel):
    """Схема для добавления пользователей."""

    nickname: str
    hashed_password: str
    salt: str


class UserAuthenticationRequest(BaseModel):
    """Схема для запроса на добавление пользователей."""

    nickname: str
    password: str


class UserAuthenticationResponse(BaseModel):
    """Схема для ответа на запрос на добавление пользователей."""

    token: str
    refresh_token: str


class UserMeResponse(BaseModel):
    id: UUID
    nickname: str
