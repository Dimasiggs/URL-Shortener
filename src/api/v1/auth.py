"""Обработчик аутентификации пользователей."""

from fastapi import APIRouter, Depends, status, HTTPException
from src.services.auth.service import AuthServicePort
from src.services.auth.dependencies import get_auth_service
from src.schemas.user import UserRegisterRequest, UserRegisterResponse

from src.core.error import UserAlreadyExistsError


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/register", response_model=UserRegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user: UserRegisterRequest,
    auth_service: AuthServicePort = Depends(get_auth_service)
):
    print(UserRegisterRequest)
    try: 
        result = await auth_service.register(user)
        print(result)

        r = UserRegisterResponse(token="token", refresh_token="refresh_token")
        return r

    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this nickname already exists",
        )


from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Заглушка: возвращает фейкового пользователя по токену."""
    try:
        print("credentialscredentialscredentialscredentialscredentialscredentials")
        print(credentials)
        # Простая проверка токена без декодирования
        # if not credentials.credentials or len(credentials.credentials) < 10:
        #     raise HTTPException(status_code=401, detail="Invalid token")
        
        # В реале: payload = jwt.decode(..., algorithms=["HS256"])
        return {"id": 123, "nickname": "Dimas"}  # заглушка из твоего фронта
    except Exception:
        raise HTTPException(status_code=401, detail="Could not validate credentials")



class UserMeResponse(BaseModel):
    id: int
    nickname: str

@router.get("/me", response_model=UserMeResponse, status_code=status.HTTP_200_OK)
async def me(
    current_user: dict = Depends(get_current_user)
):
    """Получить профиль текущего пользователя (заглушка)."""
    return UserMeResponse(
        id=current_user["id"],
        nickname=current_user["nickname"]  # из БД или сессии
    )