"""Модель ссылки для БД."""
import uuid
from sqlalchemy import UUID, Boolean, DateTime, String, func
from enum import StrEnum
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base_class import Base
from src.schemas.user import UserSchemaBase as UserSchema




class Link(Base):
    """Модель ссылки для БД."""

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )

    original_url: Mapped[Optional[str]] = mapped_column(
        String(2048),
        nullable=False
    )

    short_code: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=False,
        unique=True,
        index=True
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    
    expired_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    
    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    # def to_read_model(self) -> UserSchema:
    #     """Возвращает UserSchema из модели."""
    #     return UserSchema(
    #         id=self.id,
    #         nickname=self.nickname,
    #     )