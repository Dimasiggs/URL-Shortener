from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from uuid import UUID

from src.auth.exceptions import UserAlreadyExistsError
from src.auth.interfaces import AuthRepositoryPort
from src.users.models import User
from src.users.schemas import UserSchemaAdd



class AuthRepository(AuthRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_user(self, user: UserSchemaAdd) -> User:
        db_user = User(nickname=user.nickname, hashed_password=user.hashed_password, salt=user.salt)
        self.session.add(db_user)

        try:
            await self.session.commit()
            await self.session.refresh(db_user)

            return db_user.to_read_model()
        except IntegrityError:
            await self.session.rollback()
            raise UserAlreadyExistsError("User already exists")

    # async def login(self, user: UserSchemaAdd) -> UserAuthenticationResponse:
    #     db_user = User(nickname=user.nickname, hashed_password=user.hashed_password)
    #     self.session.add(db_user)

    async def get_id_by_name(self, user_nickname: str) -> UUID:
        query = (
            select(User)
            .where(User.nickname == user_nickname)
        )
        res = await self.session.execute(query)
        
        user = res.scalars().one()

        return user.id

    async def get_user_hashed_password(self, user_id: UUID) -> str:
        query = (
            select(User)
            .where(User.id == user_id)
        )
        res = await self.session.execute(query)
        
        user = res.scalars().one()

        return user.hashed_password

    async def get_user_salt(self, user_id: UUID) -> str:
        query = (
            select(User)
            .where(User.id == user_id)
        )
        res = await self.session.execute(query)
        
        user = res.scalars().one()

        return user.salt
    
    async def get_name(self, user_id: UUID) -> str:
        query = (
            select(User)
            .where(User.id == user_id)
        )
        res = await self.session.execute(query)
        
        user = res.scalars().one()

        return user.nickname
