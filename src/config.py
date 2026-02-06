"""Настройки для всего проекта."""

import os
from dotenv import load_dotenv
from typing import List

load_dotenv(override=True)


class Settings:
    APP_VERSION: str = "0.0.1"

    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "fastapi_db")

    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/fastapi_db")

    # CORS настройки
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    PEPPER: str = os.getenv("PEPPER", "pepper")


settings = Settings()
