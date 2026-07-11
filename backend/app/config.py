from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# .env único compartilhado entre o docker-compose e o backend
ROOT_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str


settings = Settings()
