from hashlib import sha256
from os import urandom

from src.utils import singleton
from src.auth.interfaces import HasherPort, AuthRepositoryPort, AuthServicePort
from src.users.schemas import UserRegisterRequest, UserSchemaAdd
from src.users.models import User



@singleton
class Hasher(HasherPort):
    def __init__(self, pepper: str, salt_len: int = 5):
        self.salt_len = salt_len
        self.pepper = pepper
    
    def encode(self, text: str, salt: str) -> str:
        data = text + salt + self.pepper
        data = data.encode()
        hashed_data = sha256(data).hexdigest()

        return hashed_data

    def verify(self, text: str, salt: str, hashed_text: str) -> bool:
        return self.encode(text, salt) == hashed_text

    @property
    def salt(self) -> str:
        return urandom(self.salt_len).hex()



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
