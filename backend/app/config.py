"""
Application configuration using pydantic-settings.
Reads from environment variables with .env file support.
"""

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Database - separate components for flexibility (Docker standard)
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "imagehosting"

    @computed_field
    @property
    def database_url(self) -> str:
        """Build async database URL from components."""
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    # JWT Authentication
    jwt_secret_key: str = "change-me-in-production-use-a-long-random-string"
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 10080  # 7 days

    # Cloudflare R2
    r2_account_id: str = ""
    r2_token: str = ""
    r2_access_key: str = ""
    r2_secret_key: str = ""
    r2_bucket_name: str = "image-hosting"
    r2_public_url: str = ""
    r2_jurisdiction_url: str = ""  # Optional: custom S3 endpoint

    # Application
    frontend_url: str = "http://localhost:5173"
    log_level: str = "DEBUG"


# Global settings instance
settings = Settings()
