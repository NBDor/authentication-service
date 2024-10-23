from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.token import TokenBlacklist
from app.schemas.token import TokenBlacklistCreate, TokenBlacklistRead


class CRUDToken(CRUDBase[TokenBlacklist, TokenBlacklistCreate, TokenBlacklistRead]):
    def is_token_blacklisted(self, db: Session, token: str) -> bool:
        return bool(self.get_by_filter(db, filter_params={"token": token}))


token = CRUDToken(TokenBlacklist)
