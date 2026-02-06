"""Модель ссылки для БД."""

import uuid
from sqlalchemy import UUID, Boolean, DateTime, String, func, Integer
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base
from src.links.schemas import LinkSchemaFull


class Link(Base):
    """Модель ссылки для БД."""

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    original_url: Mapped[Optional[str]] = mapped_column(String(2048), nullable=False)

    short_code: Mapped[Optional[str]] = mapped_column(
        String(20), nullable=False, unique=True, index=True
    )

    clicks: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), index=True, nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    def to_read_model(self) -> LinkSchemaFull:
        """Возвращает LinkSchemaFull из модели."""
        return LinkSchemaFull(
            id=self.id,
            original_url=self.original_url,
            short_code=self.short_code,
            owner_id=self.owner_id,
            created_at=self.created_at,
            expires_at=self.expires_at,
            is_active=self.is_active,
            clicks=self.clicks,
        )
