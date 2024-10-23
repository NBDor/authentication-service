# app/db/base.py
from typing import Any
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all database models"""

    id: Mapped[Any] = mapped_column(primary_key=True)
