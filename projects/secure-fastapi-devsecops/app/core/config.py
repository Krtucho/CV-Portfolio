from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str = "Secure FastAPI Microservice"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    API_V1_STR: str = "/api/v1"

    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "app"
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = "app"
    DATABASE_URL: str = ""

    REDIS_URL: str = "redis://localhost:6379/0"

    JWT_SECRET_KEY: str = ""
    JWT_ALGORITHM: str = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    SENTRY_DSN: str = ""

    RATE_LIMIT_PER_USER: int = 100
    RATE_LIMIT_PER_IP: int = 1000
    RATE_LIMIT_WINDOW_SECONDS: int = 60

    AWS_REGION: str = "us-east-1"
    AWS_SECRETS_NAME: str = ""

    @property
    def database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
