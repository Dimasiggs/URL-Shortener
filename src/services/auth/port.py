from typing import Protocol
from src.models.user import User
from src.schemas.user import UserRegisterRequest

class AuthServicePort(Protocol):
    async def register(self, user: UserRegisterRequest) -> User: ...
    async def get_user(self, user: UserRegisterRequest) -> User: ...