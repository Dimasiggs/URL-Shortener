from typing import Protocol
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from src.users.schemas import (
    UserAuthenticationResponse,
    UserAuthenticationRequest,
)


class AuthRepositoryPort(Protocol):
    def __init__(self, session: AsyncSession) -> None: ...
    async def add_user(self, nickname: str, hashed_password: str, salt: str) -> UUID: ...
    async def get_id_by_name(self, user_nickname: str) -> UUID: ...
    async def get_user_hashed_password(self, user_id: UUID) -> str: ...
    async def get_user_salt(self, user_id: UUID) -> str: ...
    async def get_name(self, user_id: UUID) -> str: ...


class AuthServicePort(Protocol):
    async def register(self, user: UserAuthenticationRequest) -> UserAuthenticationResponse: ...
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

    def encode(self, user_id: UUID) -> str:
        """
        Docstring for encode
        
        :return: 
        :rtype: str
        """
        ...

    def decode(self, access_token: str) -> dict:
        """
        Docstring for decode
        
        :return: {"id": str, "exp": int}
        :rtype: dict
        """
        ...
