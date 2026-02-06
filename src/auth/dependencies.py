from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.auth.services import AuthService

from src.auth.interfaces import AuthServicePort
from src.auth.interfaces import HasherPort
from src.auth.interfaces import AuthRepositoryPort


from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.repositories.auth import AuthRepository

from src.database import get_session


from src.auth.utils import Hasher
from src.config import settings


async def get_hasher() -> HasherPort:
    pepper = settings.PEPPER
    return Hasher(pepper)


async def get_auth_repository(
    db: AsyncSession = Depends(get_session),
) -> AuthRepositoryPort:
    return AuthRepository(db)


async def get_auth_service(
    hasher: HasherPort = Depends(get_hasher),
    auth_repository: AuthRepositoryPort = Depends(get_auth_repository),
) -> AuthServicePort:
    return AuthService(hasher, auth_repository)


security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """Заглушка: возвращает фейкового пользователя по токену."""
    """Получение текущего пользователя"""
    try:
        # payload = jwt.decode(..., algorithms=["HS256"])
        return {"id": 123, "nickname": "Dimas"}  # заглушка
    except Exception:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


async def get_auth_repository(
    db: AsyncSession = Depends(get_session),
) -> AuthRepositoryPort:
    return AuthRepository(db)
