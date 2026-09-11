from app.domains.permission import Permission
from app.domains.role import Role
from app.exceptions.exceptions import AlreadyExistsError, NotFoundError
from app.repositories.permision_repository import PermissionRepository
from app.repositories.role_permission_repository import RolePermissionRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.user_role_repository import UserRoleRepository


class RolePermissionService:
    def __init__(
        self,
        role_repository: RoleRepository,
        permission_repository: PermissionRepository,
        role_permission_repository: RolePermissionRepository,
        user_role_repository: UserRoleRepository,
    ):
        self.role_repository = role_repository
        self.permission_repository = permission_repository
        self.role_permission_repository = role_permission_repository
        self.user_role_repository = user_role_repository

    # Role-related methods
    def get_role_by_id(self, role_id: int) -> Role:
        role = self.role_repository.get_by_id(role_id)
        if role is None:
            raise NotFoundError("Role", "role_id", str(role_id))
        return role

    def create_role(self, role_name: str, role_description: str | None = None) -> Role:
        existing = self.role_repository.get_by_name(role_name)
        if existing is not None:
            raise AlreadyExistsError("Role", "role_name", role_name)
        return self.role_repository.create(role_name, role_description)

    def update_role(
        self, role_id: int, role_name: str, role_description: str | None = None
    ) -> Role:
        self.get_role_by_id(role_id)
        return self.role_repository.update(role_id, role_name, role_description)

    def delete_role(self, role_id: int) -> None:
        self.get_role_by_id(role_id)
        return self.role_repository.delete(role_id)

    # Permission-related methods
    def get_permission_by_id(self, permission_id: int) -> Permission:
        permission = self.permission_repository.get_by_id(permission_id)
        if permission is None:
            raise NotFoundError("Permission", "permission_id", str(permission_id))
        return permission

    def get_permission_by_name(self, name: str) -> Permission:
        permission = self.permission_repository.get_by_name(name)
        if permission is None:
            raise NotFoundError("Permission", "name", name)
        return permission

    def get_permissions(self) -> list[Permission]:
        return self.permission_repository.get_all()

    def get_roles(self) -> list[Role]:
        return self.role_repository.get_all()

    # User-Role-related methods
    def assign_role_to_user(self, user_id: int, role_id: int) -> None:
        if self.user_role_repository.user_has_role(user_id, role_id):
            raise AlreadyExistsError(
                "UserRole", "user_id|role_id", f"{user_id}|{role_id}"
            )
        self.user_role_repository.assign(user_id, role_id)

    def revoke_role_from_user(self, user_id: int, role_id: int) -> None:
        if not self.user_role_repository.user_has_role(user_id, role_id):
            raise NotFoundError("UserRole", "user_id|role_id", f"{user_id}|{role_id}")
        self.user_role_repository.revoke(user_id, role_id)

    def get_roles_by_user_id(self, user_id: int) -> list[Role]:
        return self.user_role_repository.get_roles_by_user_id(user_id)

    def user_has_role(self, user_id: int, role_id: int) -> bool:
        return self.user_role_repository.user_has_role(user_id, role_id)

    # Role-Permission-related methods
    def assign_permission_to_role(self, role_id: int, permission_id: int) -> None:
        if self.role_permission_repository.role_has_permission(role_id, permission_id):
            raise AlreadyExistsError(
                "RolePermission", "role_id|permission_id", f"{role_id}|{permission_id}"
            )
        self.role_permission_repository.assign(role_id, permission_id)

    def revoke_permission_from_role(self, role_id: int, permission_id: int) -> None:
        if not self.role_permission_repository.role_has_permission(
            role_id, permission_id
        ):
            raise NotFoundError(
                "RolePermission", "role_id|permission_id", f"{role_id}|{permission_id}"
            )
        self.role_permission_repository.revoke(role_id, permission_id)

    def get_permissions_by_role_id(self, role_id: int) -> list[Permission]:
        return self.role_permission_repository.get_permissions_by_role_id(role_id)

    def role_has_permission(self, role_id: int, permission_id: int) -> bool:
        return self.role_permission_repository.role_has_permission(
            role_id, permission_id
        )
