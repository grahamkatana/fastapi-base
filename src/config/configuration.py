from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DATABASE_URL: str = "mysql+aiomysql://root@localhost:3306/test_db"
    SECRET_KEY: str = "your-secret-key-change-this"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    STORAGE_PATH: str = "storage/reports"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
