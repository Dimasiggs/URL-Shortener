from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from src.core.error import UserAlreadyExistsError
from src.repositories.auth_port import AuthRepositoryPort
from src.models.user import User
from src.schemas.user import UserSchemaAdd

class AuthRepository(AuthRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def register(self, user: UserSchemaAdd) -> User:
        db_user = User(
            nickname=user.nickname,
            hashed_password=user.hashed_password
        )
        self.session.add(db_user)

        try:
            await self.session.commit()
            await self.session.refresh(db_user)
            return db_user.to_read_model()
        except IntegrityError:
            await self.session.rollback()
            raise UserAlreadyExistsError("User already exists")
