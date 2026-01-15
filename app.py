"""Основной модуль для запуска сервера."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import logging

from fastapi.staticfiles import StaticFiles

# from core.config import Settings
from src.api.api_routers import all_routers as api_routers


# settings = Settings()

# Логгирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Whisp_server")

app = FastAPI(
    title="settings.APP_TITLE", version="settings.APP_VERSION",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # settings.ALLOWED_ORIGINS
    allow_credentials=True, # settings.ALLOW_CREDENTIALS
    allow_methods=["*"],
    allow_headers=["*"]
)


# проверка состояния
@app.get("/health", tags=["health"])
def root():
    """Эндпоинт для проверки состояния сервера."""
    return {"status": "ok", "version": "settings.APP_VERSION"}


for router in api_routers:
    app.include_router(router, prefix="/api/v1")



app.mount("/", StaticFiles(directory="src/static"), name="static")

if __name__ == "__main__":
    import uvicorn
    server_port = int(os.getenv("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=server_port, reload=True)
