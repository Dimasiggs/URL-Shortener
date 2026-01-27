from typing import List, Protocol
from uuid import UUID

from src.repositories.link_port import LinkRepositoryPort
from src.models.link import Link
from src.schemas.link import LinkResponse, LinkSchemaAdd, LinksListResponse


class CodeGeneratorPort(Protocol):
    def generate(self) -> str: ...


class LinkServicePort(Protocol):
    def __init__(self, code_generator: CodeGeneratorPort, repository: LinkRepositoryPort) -> None: ...
    async def create(self, link_schema: LinkSchemaAdd) -> LinksListResponse: ...
    async def get_by_user_id(self, user_id: UUID, limit: int = 1, page: int = 1) -> LinksListResponse: ...
    async def get_by_short_code(self, short_code: str) -> LinkResponse: ...
