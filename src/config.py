import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV = os.path.join(os.path.dirname(__file__), ".env")
PRIVATE_PATH = Path(__file__).parent / "certs/jwt-private.pem"
PUBLIC_PATH = Path(__file__).parent / "certs/jwt-public.pem"


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    PRIVATE_KEY_PATH: Path = PRIVATE_PATH
    PUBLIC_KEY_PATH: Path = PUBLIC_PATH
    ALGORITHM: str = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    @property
    def DATABASE_URL_asyncpg(self):
        # postgresql+asyncpg://postgres:postgres@localhost:5432/sa
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=DOTENV)


settings = Settings()
