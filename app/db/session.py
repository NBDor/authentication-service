from typing import cast
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Cast to str because we know it's not None after config validation
db_uri = cast(str, settings.SQLALCHEMY_DATABASE_URI)
engine = create_engine(
    db_uri,
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
