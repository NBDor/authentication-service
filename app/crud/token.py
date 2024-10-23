from typing import Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.token import TokenBlacklist
from app.schemas.token import TokenBlacklistCreate, TokenBlacklistRead


class CRUDToken(CRUDBase[TokenBlacklist, TokenBlacklistCreate, TokenBlacklistRead]):
    def get_by_token(self, db: Session, token: str) -> Optional[TokenBlacklist]:
        return db.query(self.model).filter(self.model.token == token).first()

    def is_token_blacklisted(self, db: Session, token: str) -> bool:
        return bool(self.get_by_token(db, token))


token = CRUDToken(TokenBlacklist)
