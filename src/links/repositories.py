from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.links.models import Link
from src.links.schemas import LinkSchemaAdd, LinkSchemaFull, LinkResponse, LinksListResponse
from src.links.exceptions import DuplicateCodeError
from src.links.interfaces import LinkRepositoryPort



class LinkRepository(LinkRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, link: LinkSchemaAdd) -> LinkSchemaFull:
        db_link = Link(
            original_url=link.original_url,
            short_code=link.short_code,
            owner_id=link.owner_id,
            expires_at=link.expires_at
        )
        self.session.add(db_link)
        try:
            await self.session.commit()
            await self.session.refresh(db_link)
            return db_link.to_read_model()
        except IntegrityError:
            await self.session.rollback()
            raise DuplicateCodeError("Code already exists")

    async def get_by_user_id(self, user_id: UUID, offset: int = 0, limit: int = None) -> LinksListResponse:
        query = (
            select(Link)
            .where(Link.owner_id == user_id)
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(query)
        items = result.scalars().all()
        links = LinksListResponse(items=[i.to_read_model() for i in items], total=len(items))

        return links
    
    async def get_by_short_code(self, short_code: str) -> LinkResponse:
        query = (
            select(Link)
            .where(Link.short_code == short_code)
        )
        result = await self.session.execute(query)
        link = result.scalars().one()
        return link.to_read_model()
