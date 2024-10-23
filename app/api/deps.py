from typing import Generator, Annotated, Dict, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError

from app.core.config import settings
from app.db.session import SessionLocal
from app.core.security import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


def get_db() -> Generator[Session, None, None]:
    """
    Database dependency that provides a SQLAlchemy session.
    Ensures the session is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> Dict[str, Any]:
    """
    Get the current authenticated user from the token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = verify_access_token(token)
        if payload is None:
            raise credentials_exception

        username = payload.get("sub")
        if username is None:
            raise credentials_exception

        # Here we'd typically fetch the user from the database
        # For now, we'll return the token payload
        return {"username": str(username)}

    except (JWTError, ValueError):
        raise credentials_exception


async def get_current_active_user(
    current_user: Annotated[Dict[str, Any], Depends(get_current_user)]
) -> Dict[str, Any]:
    """
    Get the current active user.
    """
    if not current_user.get("is_active", True):  # Default to True for now
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user
