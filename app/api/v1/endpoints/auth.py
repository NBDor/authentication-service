from datetime import timedelta
from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_access_token,
    verify_refresh_token,
)
from app.schemas.auth import (
    Token,
    TokenPayload,
    AuthResponse,
    RefreshTokenRequest,
)
from app.api import deps
from app.core.config import settings
from app.services.user import verify_user_credentials

router = APIRouter()


@router.post("/login", response_model=AuthResponse)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(deps.get_db)],
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    # Here we'll make a request to User Management service to verify credentials
    # For now, we'll raise an error
    if not verify_user_credentials(form_data.username, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": form_data.username})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token_data: RefreshTokenRequest,
    db: Annotated[Session, Depends(deps.get_db)],
) -> Any:
    """
    Refresh token endpoint to get a new access token.
    """
    try:
        payload = verify_refresh_token(refresh_token_data.refresh_token)
        username = str(payload.get("sub"))  # Explicitly convert to str
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate refresh token",
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/verify", response_model=TokenPayload)
async def verify_token(token: str, db: Annotated[Session, Depends(deps.get_db)]) -> Any:
    """
    Verify a token and return its payload.
    This endpoint is mainly for internal service-to-service communication.
    """
    try:
        payload = verify_access_token(token)
        return payload
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate token",
        )


@router.post("/logout")
async def logout(
    db: Annotated[Session, Depends(deps.get_db)],
    current_user: Annotated[Any, Depends(deps.get_current_user)],
) -> Any:
    """
    Logout endpoint - invalidate the current token.
    """
    # Here we would typically:
    # 1. Add the token to a blacklist
    # 2. Clear any session data
    # For now, we'll just return success
    return {"message": "Successfully logged out"}
