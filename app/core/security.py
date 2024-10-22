from datetime import datetime, timedelta
from typing import Any, Dict, Optional, TypedDict
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenPayload(TypedDict):
    exp: datetime
    type: str
    iat: datetime
    sub: str


def create_access_token(
    data: Dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """Create JWT access token"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire, "type": "access", "iat": datetime.utcnow()})

    encoded_jwt: str = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(
    data: Dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """Create JWT refresh token"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({"exp": expire, "type": "refresh", "iat": datetime.utcnow()})

    encoded_jwt: str = jwt.encode(
        to_encode, settings.JWT_REFRESH_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def verify_access_token(token: str) -> Dict[str, Any]:
    """Verify an access token"""
    try:
        decoded_token: Dict[str, Any] = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        if decoded_token.get("type") != "access":
            raise jwt.JWTError("Invalid token type")
        return decoded_token
    except JWTError:
        raise ValueError("Invalid token")


def verify_refresh_token(token: str) -> Dict[str, Any]:
    """Verify a refresh token"""
    try:
        decoded_token: Dict[str, Any] = jwt.decode(
            token, settings.JWT_REFRESH_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        if decoded_token.get("type") != "refresh":
            raise jwt.JWTError("Invalid token type")
        return decoded_token
    except JWTError:
        raise ValueError("Invalid token")
