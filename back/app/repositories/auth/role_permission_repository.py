from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.auth import Permission, RolePermission, UserRole


class RolePermissionRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_permissions_by_role_id(self, role_id: int) -> list[Permission]:
        stmt = (
            select(Permission)
            .join(RolePermission, RolePermission.permission_id == Permission.id)
            .where(RolePermission.role_id == role_id)
            .order_by(Permission.name)
        )
        return list(self._session.scalars(stmt))

    def role_has_permission(self, role_id: int, permission_id: int) -> bool:
        assignment = self._session.get(
            RolePermission,
            {"role_id": role_id, "permission_id": permission_id},
        )
        return assignment is not None

    def get_permissions_by_user_id(self, user_id: int) -> list[Permission]:
        stmt = (
            select(Permission)
            .join(RolePermission, RolePermission.permission_id == Permission.id)
            .join(UserRole, UserRole.role_id == RolePermission.role_id)
            .where(UserRole.user_id == user_id)
            .distinct()
            .order_by(Permission.name)
        )
        return list(self._session.scalars(stmt))
