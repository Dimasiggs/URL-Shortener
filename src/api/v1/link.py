from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from src.schemas.link import LinksListResponse, LinkResponse  # твои схемы
from src.services.link import get_link_service, LinkService

router = APIRouter(tags=["Links"])

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Заглушка: возвращает фейкового пользователя по токену."""
    try:
        return {"id": "123e4567-e89b-12d3-a456-426614174000", "nickname": "Dimas"}  # заглушка из твоего фронта
    except Exception:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


@router.get("/links", response_model=LinksListResponse, status_code=200)
async def get_links(
    current_user: dict = Depends(get_current_user),
    page: int = Query(1, ge=1),
    limit: int = Query(1, le=100),
    link_service: LinkService = Depends(get_link_service)
):
    links = await link_service.get_by_user_id(current_user["id"], limit, page-1)

    return links
