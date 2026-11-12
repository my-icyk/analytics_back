from datetime import datetime

from sqlalchemy import BigInteger, Identity, String, text
from sqlalchemy.dialects.mssql import DATETIME2
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Role(Base):
    __tablename__ = "roles"
    __table_args__ = {"schema": "api"}

    id: Mapped[int] = mapped_column(
        BigInteger, Identity(start=1, increment=1), primary_key=True
    )
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(
        DATETIME2(precision=0), server_default=text("GETDATE()")
    )


class Permission(Base):
    __tablename__ = "permissions"
    __table_args__ = {"schema": "api"}

    id: Mapped[int] = mapped_column(
        BigInteger, Identity(start=1, increment=1), primary_key=True
    )
    name: Mapped[str] = mapped_column(String(150), unique=True)
