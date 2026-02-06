from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from src.links.dependencies import get_link_service
from src.links.interfaces import LinkServicePort
from src.config import settings
from src.auth.router import router as auth_router
from src.links.router import router as links_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # settings.ALLOWED_ORIGINS
    allow_credentials=True, # settings.ALLOW_CREDENTIALS
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/health", tags=["health"])
def root():
    """Эндпоинт для проверки состояния сервера."""
    return {"status": "ok", "version": settings.APP_VERSION}


app.include_router(auth_router, prefix="/api/v1")
app.include_router(links_router, prefix="/api/v1")


@app.get("/r/{short_code}")
async def redirect_to_original(
    short_code: str,
    link_service: LinkServicePort = Depends(get_link_service)
    ):
    # Получаем оригинальную ссылку из репозитория
    link = await link_service.get_by_short_code(short_code)
    original_url = link.original_url
    return RedirectResponse(url=original_url, status_code=302)


app.mount("/", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    server_port = int(os.getenv("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=server_port, reload=True)
