from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )

    DATABASE_URL: str = ""
    SECRET_KEY: str = ""
    ALGORITHM: str = ""

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 2

    # Local development uses HTTP; set COOKIE_SECURE=True in production HTTPS.
    COOKIE_SECURE: bool = False

    # query limits for get all methods
    PAGE_LIMIT: int = 10


@lru_cache
def get_settings():
    return Settings()
