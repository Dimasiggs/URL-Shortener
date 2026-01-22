"""Схемы для пользователя."""

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from pydantic.config import ConfigDict


class LinkSchemaBase(BaseModel):
    """Базовая схема для ссылок, от которой наследуется большинство схем."""

    id: UUID
    original_url: str

    model_config = ConfigDict(from_attributes=True)


class LinkSchemaAdd(BaseModel):
    """Схема для добавления ссылок."""

    original_url: str
    # short_code: str
    owner_id: UUID
    expires_at: Optional[datetime] = None

    def check_expiration(self) -> bool:
        """Проверяет, истекла ли ссылка."""
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at


class LinkSchemaFull(LinkSchemaBase):
    """Схема для отображения данных ссылки."""

    short_code: str
    owner_id: UUID
    created_at: datetime
    expires_at: Optional[datetime] = None
    is_active: bool
