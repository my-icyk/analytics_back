from datetime import datetime

from sqlalchemy import BigInteger, Identity, String, func, select, text
from sqlalchemy.dialects.mssql import DATETIME2
from sqlalchemy.orm import Mapped, column_property, mapped_column

from app.db.base import Base

from .assignments import RolePermission, UserRole


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
    users_count: Mapped[int] = column_property(
        select(func.count())
        .select_from(UserRole)
        .where(UserRole.role_id == id)
        .correlate_except(UserRole)
        .scalar_subquery()
    )

    permissions_count: Mapped[int] = column_property(
        select(func.count())
        .select_from(RolePermission)
        .where(RolePermission.role_id == id)
        .correlate_except(RolePermission)
        .scalar_subquery()
    )


class Permission(Base):
    __tablename__ = "permissions"
    __table_args__ = {"schema": "api"}

    id: Mapped[int] = mapped_column(
        BigInteger, Identity(start=1, increment=1), primary_key=True
    )
    name: Mapped[str] = mapped_column(String(150), unique=True)
