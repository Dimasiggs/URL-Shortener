"""Схемы для Ссылок."""

from datetime import datetime
from typing import List, Optional
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
    short_code: str
    owner_id: UUID
    expires_at: Optional[datetime] = None

    def check_expiration(self) -> bool:
        """Проверяет, истекла ли ссылка."""
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at


class LinkSchemaAddResponse(BaseModel):
    """Схема для добавления ссылок."""

    original_url: str
    short_code: str
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
    clicks: int


class LinkResponse(BaseModel):
    id: str
    short_code: str
    original_url: str
    clicks: int
    created_at: str  # ISO формат


class LinksListResponse(BaseModel):
    items: List[LinkSchemaFull]
    total: int
