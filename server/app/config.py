"""Einstellungen aus Umgebungsvariablen bzw. .env."""

from functools import lru_cache
from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str
    # Ohne Passwort und Secret startet der Server absichtlich nicht.
    app_password: SecretStr = Field(min_length=8)
    auth_secret: SecretStr = Field(min_length=32)
    cookie_secure: bool = True
    session_hours: int = Field(default=720, ge=1)
    upload_dir: Path = Path("uploads")
    cas_timeout_seconds: float = Field(default=5, gt=0, le=60)
    cas_memory_mb: int = Field(default=2048, ge=512)
    cas_max_workers: int = Field(default=2, ge=1, le=16)


@lru_cache
def get_settings() -> Settings:
    return Settings()
