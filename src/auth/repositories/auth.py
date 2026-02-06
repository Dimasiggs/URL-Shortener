from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.auth.exceptions import UserAlreadyExistsError
from src.auth.interfaces import AuthRepositoryPort
from src.users.models import User
from src.users.schemas import UserSchemaAdd, UserRegisterResponse


class AuthRepository(AuthRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def register(self, user: UserSchemaAdd) -> User:
        db_user = User(nickname=user.nickname, hashed_password=user.hashed_password)
        self.session.add(db_user)

        try:
            await self.session.commit()
            await self.session.refresh(db_user)

            return db_user.to_read_model()
        except IntegrityError:
            await self.session.rollback()
            raise UserAlreadyExistsError("User already exists")

    def login(self, user: UserSchemaAdd) -> UserRegisterResponse:
        db_user = User(nickname=user.nickname, hashed_password=user.hashed_password)
        self.session.add(db_user)
