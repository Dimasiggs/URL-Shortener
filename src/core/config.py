"""Всякие настройки для всего проекта."""

from typing import List
import os
import secrets
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv(override=True)


# Переделать настройки.
class Settings:
    """Настройки приложения."""

    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 24 * 8))  # 8 дней
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    JWT_AUDIENCE: str = os.getenv("JWT_AUDIENCE", "*")
    JWT_ISSUER: str = os.getenv("JWT_ISSUER", "http://localhost:8000")
    ALLOWED_ORIGINS: list = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
    ALLOW_CREDENTIALS: bool = os.getenv("ALLOW_CREDENTIALS", "False").lower() in ("true", "1", "t")

    # CORS настройки
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    def __init__(self):
        """Инициализация конфига."""
        cors_origins = os.getenv("BACKEND_CORS_ORIGINS", "*")
        if cors_origins != "*":
            if cors_origins.startswith("[") and cors_origins.endswith("]"):
                # Парсинг JSON-форматированного списка
                import json
                self.BACKEND_CORS_ORIGINS = json.loads(cors_origins)
            else:
                # Parse comma-separated list
                self.BACKEND_CORS_ORIGINS = [i.strip() for i in cors_origins.split(",")]

    # Настройки базы данных
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "fastapi_db")

    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/fastapi_db")

    CLIENT_IDS: str = os.getenv("CLIENT_IDS", "")
    APP_TITLE: str = os.getenv("APP_TITLE", "Whisp Server")
    APP_VERSION: str = os.getenv("APP_VERSION", "0.1.0")

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        """Construct database URI from components using standard psycopg2."""
        # Использование синхронного драйвера для совместимости с Python 3.13
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"


settings = Settings()
