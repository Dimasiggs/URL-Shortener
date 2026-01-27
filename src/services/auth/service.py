# from src.services.auth_port import AuthServicePort
from src.schemas.user import UserRegisterRequest, UserRegisterResponse, UserSchemaAdd

from src.repositories.auth_port import AuthRepositoryPort
from src.services.hasher_port import HasherPort

from src.models.user import User


from typing import Protocol

class AuthServicePort(Protocol):
    async def register(self, user: UserRegisterRequest) -> User: ...


class AuthService(AuthServicePort):
    def __init__(self, hasher: HasherPort, auth_repository: AuthRepositoryPort):
        self.hasher = hasher
        self.auth_repository = auth_repository

    async def register(self, user: UserRegisterRequest) -> User:

        salt = self.hasher.salt
        hashed_password = self.hasher.encode(user.password, salt)

        add_user = UserSchemaAdd(nickname=user.nickname, hashed_password=hashed_password)
        
        user_model: User = await self.auth_repository.register(add_user)

        return user_model

