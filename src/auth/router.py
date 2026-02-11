"""Обработчик аутентификации пользователей."""

from fastapi import APIRouter, Depends, HTTPException, status

from src.auth.dependencies import get_current_user

from src.auth.interfaces import AuthServicePort

from src.auth.dependencies import get_auth_service
from src.users.schemas import UserAuthenticationRequest, UserAuthenticationResponse, UserMeResponse

from src.auth.exceptions import UserAlreadyExistsError


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/login", response_model=UserAuthenticationResponse)
async def login(
    user: UserAuthenticationRequest, auth_service: AuthServicePort = Depends(get_auth_service)
) -> UserAuthenticationResponse:
    user_response = await auth_service.login(user)

    return user_response


@router.post(
    "/register",
    response_model=UserAuthenticationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user: UserAuthenticationRequest,
    auth_service: AuthServicePort = Depends(get_auth_service)
):
    print(user)
    try:
        result = await auth_service.register(user)
        print(result)

        r = UserAuthenticationResponse(token="token", refresh_token="refresh_token")  # TODO
        return r

    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this nickname already exists",
        )


@router.get("/me", response_model=UserMeResponse, status_code=status.HTTP_200_OK)
async def me(current_user: dict = Depends(get_current_user)):
    """Получить профиль текущего пользователя (заглушка)."""

    return UserMeResponse(
        id=current_user["id"],
        nickname=current_user["nickname"],
    )
