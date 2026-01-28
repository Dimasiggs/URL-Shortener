from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.schemas.link import LinksListResponse, LinkSchemaFull, LinkSchemaAddResponse, LinkSchemaAdd
from src.services.link import get_link_service
from src.services.link_port import LinkServicePort
from src.core.error import DuplicateCodeError

router = APIRouter(tags=["Links"])

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Заглушка: возвращает фейкового пользователя по токену."""
    try:
        return {"id": "123e4567-e89b-12d3-a456-426614174000", "nickname": "Dimas"}  # заглушка из твоего фронта
    except Exception:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


@router.get("/links", response_model=LinksListResponse, status_code=status.HTTP_201_CREATED)
async def get_links(
    current_user: dict = Depends(get_current_user),
    page: int = Query(1, ge=1),
    limit: int = Query(1, le=100),
    link_service: LinkServicePort = Depends(get_link_service)
):
    links = await link_service.get_by_user_id(current_user["id"], limit, page-1)

    return links

from pydantic import BaseModel
class ResponseSchema(BaseModel):
    short_url: str = "www.short-url.com"


@router.post("/links", response_model=LinkSchemaFull, status_code=status.HTTP_201_CREATED)
async def create_link(
    link: LinkSchemaAddResponse,
    current_user: dict = Depends(get_current_user),
    link_service: LinkServicePort = Depends(get_link_service)
):
    # print(link) # original_url='http://localhost:8000/index.html' short_code='slug' expires_at=datetime.datetime(2222, 2, 22, 22, 22)

    short_code = link.short_code
    if short_code is None: short_code = link_service.code_generator.generate()

    link_schema_add = LinkSchemaAdd(
        original_url=link.original_url,
        short_code=short_code,
        owner_id=current_user["id"],
        expires_at=link.expires_at
        )
    try:
    
        added_link = await link_service.create(link_schema_add)
        return added_link
    except DuplicateCodeError:
        raise ValueError("Short code already in use")


