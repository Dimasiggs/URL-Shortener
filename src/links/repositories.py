from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update, delete
from uuid import UUID

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
            expires_at=link.expires_at,
            clicks=0
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
    
    async def add_click(self, short_code: str) -> LinkResponse:
        query = (
            update(Link)
            .where(Link.short_code == short_code)
            .values(clicks=Link.clicks + 1)  # ← Ключевая часть: используем выражение из модели
            .returning(Link)
        )

        result = await self.session.execute(query)
        updated_link = result.scalar_one_or_none()

        if updated_link is None:
            raise ValueError(f"Link with code '{short_code}' not found")
        
        await self.session.commit()
        return updated_link.to_read_model()

    async def delete_by_id(self, link_id: UUID) -> None:
        print(link_id)
        print(str(link_id))
        query = (
            delete(Link)
            .where(Link.id == link_id)
        )

        await self.session.execute(query)
        await self.session.commit()
