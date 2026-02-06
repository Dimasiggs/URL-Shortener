from uuid import UUID

from src.links.models import Link
from src.links.schemas import LinkSchemaAdd, LinkResponse, LinksListResponse
from src.links.interfaces import LinkRepositoryPort, LinkServicePort, CodeGeneratorPort



class LinkService(LinkServicePort):
    def __init__(self, code_generator: CodeGeneratorPort, repository: LinkRepositoryPort):
        self.code_generator = code_generator
        self.repository = repository

    async def create(self, link_schema: LinkSchemaAdd) -> LinkResponse:
        while 1:
            link_add = Link(
                original_url=link_schema.original_url,
                short_code=self.code_generator.generate(),
                owner_id=link_schema.owner_id,
                expires_at=link_schema.expires_at
            )
        
            try:
                new_link = await self.repository.create(link_add)
                return new_link
            except Exception:
                continue
    
    async def get_by_user_id(self, user_id: UUID, limit: int = None, page: int = 0) -> LinksListResponse:
        offset = limit * page
        links = await self.repository.get_by_user_id(user_id, offset, limit)

        return links
    
    async def get_by_short_code(self, short_code: str) -> LinkResponse:
        try:    
            link = await self.repository.get_by_short_code(short_code)
            
            return link
        except:
            return LinkResponse(id="", short_code="", original_url="http://localhost:8000/index.html", clicks=0, created_at="")
