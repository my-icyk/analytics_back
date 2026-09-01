from app.core.permisions import PermissionEnum, has_permission
from app.exceptions.exceptions import (
    ForbiddenError,
    NotFoundError,
    RoleNotFoundError,
)
from app.models.role import Role
from app.models.user import User
from app.repositories.role_repository import RoleRepository


class RoleService:
    def __init__(self, role_repository: RoleRepository):
        self.role_repository = role_repository

    def create_role(
        self, name: str, description: str | None, current_user: User
    ) -> Role:
        if not has_permission(current_user, PermissionEnum.ROLES_CREATE):
            raise ForbiddenError("You dont have permission to create a role.")
        return self.role_repository.create(name, description)

    def get_role(self, role_id: int, current_user: User) -> Role:
        if not has_permission(current_user, PermissionEnum.ROLES_READ):
            raise ForbiddenError("You dont have permission to access this role's data.")
        role = self.role_repository.get_by_id(role_id)

        if role is None:
            raise RoleNotFoundError(role_id)

        return role

    def update_role(
        self,
        role_id: int,
        name: str | None,
        description: str | None,
        current_user: User,
    ) -> Role:
        if not has_permission(current_user, PermissionEnum.ROLES_UPDATE):
            raise ForbiddenError("You dont have permission to update this role.")
        role = self.role_repository.get_by_id(role_id)

        if role is None:
            raise RoleNotFoundError(role_id)

        return self.role_repository.update(role_id, name, description)

    def get_users_by_role_id(self, role_id: int, current_user: User) -> list[User]:
        if not has_permission(current_user, PermissionEnum.USER_ROLES_READ):
            raise ForbiddenError(
                "You dont have permission to access this role's users."
            )
        users = self.role_repository.get_users_by_role_id(role_id)
        if users is None:
            raise NotFoundError("Users", "role_id", role_id)
        return users
