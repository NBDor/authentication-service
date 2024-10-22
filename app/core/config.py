from functools import lru_cache
from typing import Any, List, Optional, Union
from typing_extensions import TypeAlias
from pydantic import AnyHttpUrl, Field, field_validator
from pydantic_settings import BaseSettings

# Type aliases
DatabaseValues: TypeAlias = dict[str, Any]
StrOrStrList: TypeAlias = Union[str, List[str]]


class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = Field(default="/api/v1")
    PROJECT_NAME: str = Field(default="Authentication Service")
    VERSION: str = Field(default="1.0.0")

    # Security Settings
    JWT_SECRET_KEY: str = Field(...)
    JWT_REFRESH_SECRET_KEY: str = Field(...)
    JWT_ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7)

    # CORS Settings
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = Field(default_factory=list)

    # Database Settings
    POSTGRES_SERVER: str = Field(...)
    POSTGRES_USER: str = Field(...)
    POSTGRES_PASSWORD: str = Field(...)
    POSTGRES_DB: str = Field(...)
    SQLALCHEMY_DATABASE_URI: Optional[str] = Field(default=None)

    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "allow",
    }

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: StrOrStrList) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v if isinstance(v, list) else [v]
        raise ValueError(v)

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    def assemble_db_connection(cls, v: Optional[str], info: Any) -> str:
        if isinstance(v, str):
            return v

        values = info.data
        return (
            f"postgresql://{values['POSTGRES_USER']}:"
            f"{values['POSTGRES_PASSWORD']}@"
            f"{values['POSTGRES_SERVER']}/"
            f"{values['POSTGRES_DB']}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
