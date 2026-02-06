from src.auth.interfaces import HasherPort, AuthRepositoryPort, AuthServicePort
from src.users.schemas import UserRegisterRequest, UserSchemaAdd
from src.users.models import User



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
