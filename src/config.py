from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent

class Settings(BaseSettings):
    SECRET_KEY: str
    TEMPLATES_DIR: Path = BASE_DIR / "templates"
    DATABASE_URL: str = "sqlite:///src/db.sqlite3"

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")


settings = Settings()
