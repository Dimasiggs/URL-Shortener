from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from src.models.link import Link
from src.schemas.link import LinkSchemaAdd
from src.core.error import DuplicateCodeError
from src.repositories.link_port import LinkRepositoryPort


class LinkRepository(LinkRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, link: LinkSchemaAdd) -> Link:
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
