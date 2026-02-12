from src.auth.interfaces import HasherPort, AuthRepositoryPort, AuthServicePort, JWTServicePort
from src.users.schemas import UserAuthenticationRequest, UserAuthenticationResponse
from src.auth.exceptions import IncorrectPassword


class AuthService(AuthServicePort):
    def __init__(self, hasher: HasherPort, auth_repository: AuthRepositoryPort, jwt_util: JWTServicePort):
        self.hasher = hasher
        self.auth_repository = auth_repository
        self.jwt_util = jwt_util

    async def register(self, user: UserAuthenticationRequest) -> UserAuthenticationResponse:

        salt = self.hasher.salt
        hashed_password = self.hasher.encode(user.password, salt)

        user_id = await self.auth_repository.add_user(user.nickname, hashed_password, salt)

        jwt_token = self.jwt_util.encode(user_id)

        return UserAuthenticationResponse(token=jwt_token, refresh_token="lol")

    async def login(self, user: UserAuthenticationRequest) -> UserAuthenticationResponse:
        user_id = await self.auth_repository.get_id_by_name(user.nickname)
        salt = await self.auth_repository.get_user_salt(user_id)
        hashed_password = await self.auth_repository.get_user_hashed_password(user_id)
        
        if not self.hasher.verify(user.password, salt, hashed_password):
            raise IncorrectPassword("Пароли то самое") 
        
        
        jwt_token = self.jwt_util.encode(user_id)

        return UserAuthenticationResponse(token=jwt_token, refresh_token="lol")
