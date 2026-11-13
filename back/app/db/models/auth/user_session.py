from datetime import datetime

from sqlalchemy import CHAR, BigInteger, CheckConstraint, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.mssql import DATETIME2
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class UserSession(Base):
    __tablename__ = "user_sessions"
    __table_args__ = (
        UniqueConstraint("token_hash", name="UQ_user_sessions_token_hash"),
        CheckConstraint("expires_at > created_at", name="CK_user_sessions_expiry"),
        {"schema": "api"},
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "api.users.id",
            name="FK_user_sessions_user",
            ondelete="CASCADE",
        ),
        primary_key=True,
        autoincrement=False,
    )
    token_hash: Mapped[str] = mapped_column(CHAR(64))
    created_at: Mapped[datetime] = mapped_column(DATETIME2(precision=6))
    expires_at: Mapped[datetime] = mapped_column(DATETIME2(precision=6))
