from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class TokenBlacklistBase(BaseModel):
    token: str
    expiry_date: datetime
    reason: Optional[str] = None


class TokenBlacklistCreate(TokenBlacklistBase):
    pass


class TokenBlacklistRead(TokenBlacklistBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
