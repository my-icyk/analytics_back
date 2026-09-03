from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str = ""
    SECRET_KEY: str = ""
    ALGORITHM: str = ""

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 2

    COOKIE_SECURE: bool = True

    # model_config = SettingsConfigDict(
    #     env_file=".env",
    #     env_file_encoding="utf-8",
    #     case_sensitive=True
    # )


@lru_cache
def get_settings():
    return Settings()


# For testing
if __name__ == "__main__":
    settings = get_settings()
    print(f"DATABASE_URL: {settings.DATABASE_URL}")
    print(
        f"SECRET_KEY: {settings.SECRET_KEY[:20]}..."
    )  # Only show first 10 chars for security
