from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, String, false, text, true
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "api"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(255))
    email: Mapped[str | None] = mapped_column(String(255))
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, server_default=true())
    is_admin: Mapped[bool] = mapped_column(Boolean, server_default=false())
    name: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("SYSDATETIME()"),
    )
    employee_ref: Mapped[str | None] = mapped_column(String(255))
