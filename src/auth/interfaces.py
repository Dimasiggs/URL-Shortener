from typing import Protocol
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.schemas import UserSchemaAdd, UserRegisterResponse, UserRegisterRequest, UserSchemaBase
from src.auth.schemas.token import JWTToken

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



class JWTServicePort(Protocol):
    alg: str
    secret_key: str
    exp_minutes: str

    def encode(self, user: UserSchemaBase) -> JWTToken: ...
    def decode(self, token: JWTToken) -> UserSchemaBase: ...
