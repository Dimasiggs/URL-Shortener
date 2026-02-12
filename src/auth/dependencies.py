from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.schemas import JWTToken
from src.auth.services import AuthService
from src.auth.utils import Hasher
from src.auth.utils import JWTService

from src.auth.interfaces import AuthServicePort
from src.auth.interfaces import HasherPort
from src.auth.interfaces import AuthRepositoryPort
from src.auth.interfaces import JWTServicePort

from src.auth.repositories import AuthRepository

from src.database import get_session

from src.config import settings


load_dotenv(override=True)

security = HTTPBearer()


async def get_hasher() -> HasherPort:
    pepper = settings.PEPPER
    return Hasher(pepper)


async def get_auth_repository(
    db: AsyncSession = Depends(get_session),
) -> AuthRepositoryPort:
    return AuthRepository(db)


def get_jwt_service() -> JWTServicePort:
    secret_key = settings.SECRET_KEY
    alg = settings.JWT_ALGORITHM
    exp_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    return JWTService(
        alg,
        secret_key,
        exp_minutes
    )


async def get_auth_service(
    hasher: HasherPort = Depends(get_hasher),
    auth_repository: AuthRepositoryPort = Depends(get_auth_repository),
    jwt_util: JWTServicePort = Depends(get_jwt_service)
) -> AuthServicePort:
    return AuthService(hasher, auth_repository, jwt_util)

# TODO: Перенести в папку user
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    jwt_util: JWTServicePort = Depends(get_jwt_service),
    auth_repo: AuthRepositoryPort = Depends(get_auth_repository)
) -> dict:
    """Получение id текущего пользователя"""
    try:
        print("loooooooooooooooooool")
        a = jwt_util.decode(JWTToken(access_token=credentials.credentials))
        print(a.id)
        nickname = await auth_repo.get_name(a.id)
        print(nickname)

        return {"id": a.id, "nickname": nickname}
    except Exception:
        print("KEEEEEEEEEEEEEEEEEEEEKKKK")
        raise HTTPException(status_code=401, detail="Could not validate credentials")
