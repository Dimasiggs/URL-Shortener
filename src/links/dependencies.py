import secrets
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session

from src.links.interfaces import LinkRepositoryPort
from src.links.interfaces import CodeGeneratorPort

from src.links.repositories import LinkRepository

from src.links.services.services import LinkService


# TODO: Убрать отсюда
class CodeGenerator(CodeGeneratorPort):
    def __init__(self):
        self.len = 5

    def generate(self):
        return secrets.token_hex(self.len)


def get_code_generator():
    return CodeGenerator()


def get_link_repository(db: AsyncSession = Depends(get_session)) -> LinkRepository:
    return LinkRepository(db)


async def get_link_service(
    code_generator: CodeGeneratorPort = Depends(get_code_generator),
    repository: LinkRepositoryPort = Depends(get_link_repository),
) -> LinkService:
    return LinkService(code_generator, repository)
