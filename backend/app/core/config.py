"""Core configuration — environment variables and settings."""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # App
    APP_NAME: str = "LifeOS"
    DEBUG: bool = False
    SECRET_KEY: str = "change-me-in-production"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://lifeos:lifeos@localhost:5432/lifeos"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # JWT
    JWT_SECRET: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # AI — Google Gemini
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.0-flash"

    # AI — Ollama (local fallback)
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2"

    # Whisper
    WHISPER_API_KEY: str = ""

    # Telegram
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_MINI_APP_URL: str = ""

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]

    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 100

    # Premium
    FREE_AI_MESSAGES_PER_DAY: int = 20

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
