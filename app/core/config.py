from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: str
    
    # Telegram
    TELEGRAM_BOT_TOKEN: str
    
    # App
    APP_ENV: str = "development"
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()