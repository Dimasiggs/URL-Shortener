from typing import Protocol
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from src.users.schemas import (
    UserSchemaAdd,
    UserAuthenticationResponse,
    UserAuthenticationRequest,
    UserSchemaBase,
)
from src.auth.schemas.token import JWTToken

from src.users.models import User


class AuthRepositoryPort(Protocol):
    def __init__(self, session: AsyncSession) -> None: ...
    async def add_user(self, user: UserSchemaAdd) -> User: ...
    async def login(self, user: UserSchemaAdd) -> UserAuthenticationResponse: ...
    async def get_id_by_name(self, user_nickname: str) -> UUID: ...
    async def get_user_hashed_password(self, user_id: UUID) -> str: ...
    async def get_user_salt(self, user_id: UUID) -> str: ...


class AuthServicePort(Protocol):
    async def register(self, user: UserAuthenticationRequest) -> User: ...
    async def login(self, user: UserAuthenticationRequest) -> UserAuthenticationResponse: ...


class HasherPort(Protocol):
    pepper: str
    salt_len: int

    def encode(self, text: str, salt: str) -> str: ...
    def verify(self, text: str, salt: str, hashed_text: str) -> bool: ...
    @property
    def salt(self) -> str: ...


class JWTServicePort(Protocol):
    alg: str
    secret_key: str
    exp_minutes: str

    def encode(self, user: UserSchemaBase) -> JWTToken: ...
    def decode(self, token: JWTToken) -> UserSchemaBase: ...
