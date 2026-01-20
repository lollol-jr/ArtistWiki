"""
Application Configuration
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """애플리케이션 설정"""

    # Database
    DATABASE_URL: str

    # MediaWiki
    MEDIAWIKI_API_URL: str
    MEDIAWIKI_BOT_USERNAME: str
    MEDIAWIKI_BOT_PASSWORD: str

    # AI
    OPENAI_API_KEY: str
    ANTHROPIC_API_KEY: str = ""

    # App
    SECRET_KEY: str
    DEBUG: bool = False
    ENVIRONMENT: str = "production"

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
