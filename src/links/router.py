from fastapi import APIRouter, Depends, Query, status
import uuid

from src.links.schemas import (
    LinkStatsResponse,
    LinksListResponse,
    LinkSchemaFull,
    LinkSchemaAddResponse,
    LinkSchemaAdd,
)
from src.links.dependencies import get_link_service
from src.auth.dependencies import get_current_user
from src.links.interfaces import LinkServicePort
from src.links.exceptions import DuplicateCodeError


router = APIRouter(prefix="/links", tags=["Links"])


@router.get("", response_model=LinksListResponse, status_code=status.HTTP_200_OK)
async def get_links(
    current_user: dict = Depends(get_current_user),
    page: int = Query(1, ge=1),
    limit: int = Query(1, le=100),
    link_service: LinkServicePort = Depends(get_link_service),
):
    links = await link_service.get_by_user_id(current_user["id"], limit, page - 1)

    return links


@router.post(
    "", response_model=LinkSchemaFull, status_code=status.HTTP_201_CREATED
)
async def create_link(
    link: LinkSchemaAddResponse,
    current_user: dict = Depends(get_current_user),
    link_service: LinkServicePort = Depends(get_link_service),
):
    short_code = link.short_code
    if short_code is None:
        short_code = link_service.code_generator.generate()

    link_schema_add = LinkSchemaAdd(
        original_url=link.original_url,
        short_code=short_code,
        owner_id=current_user["id"],
        expires_at=link.expires_at,
    )
    try:
        added_link = await link_service.create(link_schema_add)
        return added_link
    except DuplicateCodeError:
        raise ValueError("Short code already in use")


@router.delete("/{link_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_link(
    link_id: uuid.UUID,
    current_user: dict = Depends(get_current_user),
    link_service: LinkServicePort = Depends(get_link_service),
):
    await link_service.delete_by_id(link_id)


@router.get("/{link_id}/stats", response_model=LinkStatsResponse, status_code=status.HTTP_200_OK)
async def get_link_info(
    link_id: uuid.UUID,
    current_user: dict = Depends(get_current_user),
    link_service: LinkServicePort = Depends(get_link_service),
):
    return LinkStatsResponse(total_clicks=10, unique_ips=2, top_countries=[{"country": "Russia", "count": 100}, {"country": "USA", "count": 200}], clicks_per_day=[{"date": "2025-02-10", "count": 10}, {"date": "2026-02-10", "count": 20}, {"date": "2027-02-10", "count": 30}])
