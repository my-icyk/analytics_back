from app.core.permisions import PermissionEnum, has_permission
from app.exceptions.exceptions import ForbiddenError
from app.models.permission import Permission
from app.models.user import User
from app.repositories.permision_repository import PermissionRepository
from app.repositories.role_permission_repository import RolePermissionRepository
from app.repositories.role_repository import RoleRepository


class RolePermissionService:
    def __init__(
        self,
        role_repository: RoleRepository,
        permission_repository: PermissionRepository,
        role_permission_repository: RolePermissionRepository,
    ):
        self.role_permission_repository = role_permission_repository
        self.role_repository = role_repository
        self.permission_repository = permission_repository

    def assign_permission_to_role(
        self, role_id: int, permission_id: int, current_user: User
    ) -> None:
        if not has_permission(current_user, PermissionEnum.ROLE_PERMISSIONS_CREATE):
            raise ForbiddenError(
                "You don't have permission to assign permissions to roles."
            )
        self.role_repository.get_by_id(role_id)
        self.permission_repository.get_by_id(permission_id)

        if self.role_permission_repository.exists(role_id, permission_id):
            raise ValueError(
                f"Permission ID: {permission_id} is already assigned to role ID: {role_id}."
            )

        self.role_permission_repository.create(role_id, permission_id)

    def remove_permission_from_role(
        self, role_id: int, permission_id: int, current_user
    ) -> None:
        if not has_permission(current_user, PermissionEnum.ROLE_PERMISSIONS_DELETE):
            raise ForbiddenError(
                "You don't have permission to remove permissions from roles."
            )
        self.role_repository.get_by_id(role_id)
        self.permission_repository.get_by_id(permission_id)

        if not self.role_permission_repository.exists(role_id, permission_id):
            raise ValueError(
                f"Permission ID: {permission_id} is not assigned to role ID: {role_id}."
            )

        self.role_permission_repository.delete(role_id, permission_id)

    def get_permissions_by_role_id(
        self, role_id: int, current_user: User
    ) -> list[Permission]:
        if not has_permission(current_user, PermissionEnum.ROLE_PERMISSIONS_READ):
            raise ForbiddenError(
                "You don't have permission to view this role's permissions."
            )
        self.role_repository.get_by_id(role_id)
        return self.role_permission_repository.get_permissions_by_role_id(role_id)
