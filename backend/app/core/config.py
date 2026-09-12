from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "ACE Backend API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "ace-secret-key-change-in-production-environments"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    ALGORITHM: str = "HS256"

    DATABASE_URL: str = "sqlite+aiosqlite:///./ace.db"

    OPENROUTER_API_KEY: Optional[str] = "AQ.Ab8RN6LyhBB3tsRdrTTMlMkmbZN1Vg0g9s7N_i9XbSBuNXyOgw"
    GEMINI_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()

