from app.core.permisions import PermissionEnum, has_permission
from app.exceptions.exceptions import (
    AlreadyExistsError,
    ForbiddenError,
    NotFoundError,
)
from app.models.role import Role
from app.models.user import User
from app.repositories.role_repository import RoleRepository


class RoleService:
    def __init__(self, role_repository: RoleRepository):
        self.role_repository = role_repository

    def get_by_id(self, role_id: int, current_user: User) -> Role:
        if not has_permission(current_user, PermissionEnum.ROLES_READ):
            raise ForbiddenError("You dont have permission to access this role's data.")

        role = self.role_repository.get_by_id(role_id)

        if role is None:
            raise NotFoundError("Role", "id", role_id)

        return role

    def get_all(self, current_user: User) -> list[Role]:
        if not has_permission(current_user, PermissionEnum.ROLES_READ):
            raise ForbiddenError("You dont have permission to access roles data.")
        return self.role_repository.get_all()

    def create(self, name: str, description: str | None, current_user: User) -> Role:
        if not has_permission(current_user, PermissionEnum.ROLES_CREATE):
            raise ForbiddenError("You dont have permission to create a role.")

        if self.role_repository.get_by_name(name):
            raise AlreadyExistsError("Role", "name", name)
        role_id = self.role_repository.create(name, description)

        return self.get_by_id(role_id, current_user)

    def update(
        self,
        role_id: int,
        name: str | None,
        description: str | None,
        current_user: User,
    ) -> Role:
        if not has_permission(current_user, PermissionEnum.ROLES_UPDATE):
            raise ForbiddenError("You dont have permission to update this role.")

        self.get_by_id(role_id, current_user)

        self.role_repository.update(role_id, name, description)
        # TODO: using get_by_id again is not optimal, but for now it works, need to be refactored
        return self.get_by_id(role_id, current_user)

    def delete(self, role_id: int, current_user: User) -> None:
        if not has_permission(current_user, PermissionEnum.ROLES_DELETE):
            raise ForbiddenError("You dont have permission to delete this role.")

        self.get_by_id(role_id, current_user)

        self.role_repository.delete(role_id)

    def get_by_name(self, name: str, current_user: User) -> Role:
        if not has_permission(current_user, PermissionEnum.ROLES_READ):
            raise ForbiddenError("You dont have permission to access this role's data.")

        role = self.role_repository.get_by_name(name)

        if role is None:
            raise NotFoundError("Role", "name", name)

        return role

    # TODO: i dont like that method, need to be refactored, but for now it works
    def get_users_by_role_id(self, role_id: int, current_user: User) -> list[User]:
        if not has_permission(current_user, PermissionEnum.USER_ROLES_READ):
            raise ForbiddenError(
                "You dont have permission to access this role's users."
            )
        users = self.role_repository.get_users_by_role_id(role_id)
        if users is None:
            raise NotFoundError("Users", "role_id", role_id)
        return users
