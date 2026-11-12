from sqlalchemy import BigInteger, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class UserRole(Base):
    __tablename__ = "user_roles"
    __table_args__ = (
        PrimaryKeyConstraint("user_id", "role_id", name="PK_user_roles"),
        {"schema": "api"},
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("api.users.id", name="FK_user_roles_user", ondelete="CASCADE"),
    )
    role_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("api.roles.id", name="FK_user_roles_role", ondelete="CASCADE"),
    )


class RolePermission(Base):
    __tablename__ = "role_permissions"
    __table_args__ = (
        PrimaryKeyConstraint("role_id", "permission_id", name="PK_role_permissions"),
        {"schema": "api"},
    )

    role_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("api.roles.id", name="FK_role_permissions_role", ondelete="CASCADE"),
    )
    permission_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "api.permissions.id",
            name="FK_role_permissions_permission",
            ondelete="CASCADE",
        ),
    )
