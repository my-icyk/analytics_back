from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.auth import Permission, RolePermission, UserRole


class AuthorizationRepository:
    def __init__(self, session: Session):
        self._session = session

    def user_has_permission(self, user_id: int, permission_name: str) -> bool:
        stmt = (
            select(Permission.id)
            .select_from(UserRole)
            .join(RolePermission, RolePermission.role_id == UserRole.role_id)
            .join(Permission, Permission.id == RolePermission.permission_id)
            .where(
                UserRole.user_id == user_id,
                Permission.name == permission_name,
            )
            .limit(1)
        )
        return self._session.scalar(stmt) is not None
