from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DATABASE_URL: str = "sqlite+aiosqlite:///./astro4.db"
    SECRET_KEY: str = "change-me-in-production-secret-key-at-least-32-chars"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    FRONTEND_URL: str = "http://localhost:4321"

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def normalize_database_url(cls, v: str) -> str:
        """Normalize Render's postgres:// URL to SQLAlchemy's postgresql+psycopg2://."""
        if isinstance(v, str) and v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql+psycopg2://", 1)
        return v


settings = Settings()
