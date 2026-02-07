from typing import Protocol
from uuid import UUID

from src.links.schemas import (
    LinkResponse,
    LinkSchemaAdd,
    LinksListResponse,
    LinkSchemaFull,
    LinkSchemaBase,
)
from src.users.schemas import UserSchemaBase


class LinkRepositoryPort(Protocol):
    async def create(self, link: LinkSchemaAdd) -> LinkSchemaFull: ...
    async def deactivate(self, link: LinkSchemaBase) -> None: ...

    async def get_by_short_code(self, short_code: str) -> LinkResponse: ...
    async def get_by_user_id(
        self, user: UUID, offset: int, limit: int
    ) -> LinksListResponse: ...
    async def add_click(self, short_code: str) -> LinkResponse: ...

    async def delete_by_id(self, link_id: UUID) -> None: ...


class CodeGeneratorPort(Protocol):
    def generate(self) -> str: ...


class LinkServicePort(Protocol):
    code_generator: CodeGeneratorPort
    repository: LinkRepositoryPort

    async def create(self, link_schema: LinkSchemaAdd) -> LinkResponse: ...
    async def get_by_user_id(
        self, user_id: UUID, limit: int = None, page: int = 1
    ) -> LinksListResponse: ...
    async def get_by_short_code(self, short_code: str) -> LinkResponse: ...
    async def redirect(self, short_code: str) -> LinkResponse: ...
    async def delete_by_id(self, link_id: UUID) -> None: ...
