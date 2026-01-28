from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from fastapi import Depends
from src.services.link import get_link_service, LinkServicePort

router = APIRouter(
    prefix="/r",
    tags=["Redirect"],
)

@router.get("/{short_code}")
async def redirect_to_original(
    short_code: str,
    link_service: LinkServicePort = Depends(get_link_service)
    ):
    # Получаем оригинальную ссылку из репозитория
    link = await link_service.get_by_short_code(short_code)
    original_url = link.original_url
    return RedirectResponse(url=original_url, status_code=302)
