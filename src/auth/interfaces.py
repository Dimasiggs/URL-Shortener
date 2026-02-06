from typing import Protocol
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.schemas import UserSchemaAdd, UserRegisterResponse, UserRegisterRequest
from src.users.models import User



class AuthRepositoryPort(Protocol):
    def __init__(self, session: AsyncSession) -> None: ...
    async def register(self, user: UserSchemaAdd) -> User: ...
    async def login(self, user: UserSchemaAdd) -> UserRegisterResponse: ...



class AuthServicePort(Protocol):
    async def register(self, user: UserRegisterRequest) -> User: ...
    async def get_user(self, user: UserRegisterRequest) -> User: ...



class HasherPort(Protocol):
    pepper: str
    salt_len: int
    def encode(self, text: str, salt: str) -> str: ...
    def verify(self, text: str, salt: str, hashed_text: str) -> bool: ...
    @property
    def salt(self) -> str: ...
