from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


class Token(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    sub: Optional[str] = None
    exp: Optional[int] = None


class AuthResponse(Token):
    model_config = ConfigDict(from_attributes=True)

    refresh_token: str


class LoginRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    refresh_token: str
