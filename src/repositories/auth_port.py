from typing import Protocol
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.user import UserSchemaAdd, UserRegisterResponse
from src.models.user import User


class AuthRepositoryPort(Protocol):
    def __init__(self, session: AsyncSession) -> None: ...
    async def register(self, user: UserSchemaAdd) -> User: ...
    async def login(self, user: UserSchemaAdd) -> UserRegisterResponse: ...

