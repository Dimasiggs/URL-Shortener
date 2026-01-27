# app/application/services/auth/dependencies.py
from fastapi import Depends

from src.services.auth.service import AuthService, AuthServicePort
from src.services.hasher_port import HasherPort
from src.repositories.auth_port import AuthRepositoryPort

from src.services.hasher import get_hasher
from src.repositories.auth import get_auth_repository

async def get_auth_service(
    hasher: HasherPort = Depends(get_hasher),
    auth_repository: AuthRepositoryPort = Depends(get_auth_repository)
) -> AuthServicePort:
    return AuthService(hasher, auth_repository)
