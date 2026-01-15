"""Обработчик аутентификации пользователей."""

from uuid import uuid4
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any
# from api.dependencies import UOWDep
# from schemas.user import UserSchemaAdd
# from services.user import UsersService

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)
    

class RegisterRequest(BaseModel):
    email: str
    password: str


class RegisterResponse(BaseModel):
    token: str
    refresh_token: str


@router.post("/register", response_model=RegisterResponse)
async def register_user(
    # user: UserSchemaAdd,
    user: RegisterRequest
    # uow: UOWDep,
) -> Dict[str, Any]:
    """Регистрация пользователя."""
    token = "Token!!!!!!!!"
    refresh_token = "Refresh Token!!!!!!!!"
    #print(f"Регистрация пользователя {user.nickname, user.hashed_password}: {token, refresh_token}")
    print(RegisterRequest)
    return {"token": token, "refresh_token": refresh_token}
