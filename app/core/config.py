from typing import Any, Dict, Optional, Union, List
from pydantic import field_validator, AnyHttpUrl, PostgresDsn, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_SECRET_KEY: str
    PROJECT_NAME: str = "Authentication Service"
    
    # BACKEND_CORS_ORIGINS is a comma-separated list of origins
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database settings
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str = "5432"
    DATABASE_URL: Optional[PostgresDsn] = None
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    # Handle database URL construction after all fields are validated
    @model_validator(mode="after")
    def assemble_db_connection(self) -> "Settings":
        """Construct database URL from components after all fields are validated."""
        # If a database URL is already provided, use it
        if self.DATABASE_URL:
            self.SQLALCHEMY_DATABASE_URI = self.DATABASE_URL
            return self
            
        # Check if we have all required fields
        if (self.POSTGRES_SERVER and self.POSTGRES_USER and 
            self.POSTGRES_PASSWORD and self.POSTGRES_DB and self.POSTGRES_PORT):
            
            # Construct the PostgreSQL connection URL
            db_url = PostgresDsn.build(
                scheme="postgresql",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_SERVER,
                port=self.POSTGRES_PORT,
                path=f"{self.POSTGRES_DB}",
            )
            
            # Set both URL fields to the same value
            self.DATABASE_URL = db_url
            self.SQLALCHEMY_DATABASE_URI = db_url
            
        return self

    ENVIRONMENT: str = "production"
    
    # User service URL for authentication
    USER_SERVICE_URL: AnyHttpUrl

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )


def get_settings() -> Settings:
    return Settings()


settings = get_settings()