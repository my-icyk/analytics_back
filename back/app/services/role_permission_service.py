from app.domains.permission import Permission
from app.domains.role import Role
from app.exceptions.exceptions import AlreadyExistsError, NotFoundError
from app.repositories.permision_repository import PermissionRepository
from app.repositories.role_permission_repository import RolePermissionRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.repositories.user_role_repository import UserRoleRepository


class RolePermissionService:
    def __init__(
        self,
        role_repository: RoleRepository,
        permission_repository: PermissionRepository,
        role_permission_repository: RolePermissionRepository,
        user_role_repository: UserRoleRepository,
        user_repository: UserRepository,
    ):
        self.role_repository = role_repository
        self.permission_repository = permission_repository
        self.role_permission_repository = role_permission_repository
        self.user_role_repository = user_role_repository
        self.user_repository = user_repository

    # Role-related methods
    def get_role_by_id(self, role_id: int) -> Role:
        role = self.role_repository.get_by_id(role_id)
        if role is None:
            raise NotFoundError("Role", "role_id", str(role_id))
        return role

    def get_user_by_id(self, user_id: int):
        user = self.user_repository.get_by_id(user_id)
        if user is None:
            raise NotFoundError("User", "user_id", str(user_id))
        return user

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

    def get_permissions_by_user_id(self, user_id: int) -> list[Permission]:
        return self.role_permission_repository.get_permissions_by_user_id(user_id)

    def get_permissions(self) -> list[Permission]:
        return self.permission_repository.get_all()

    def get_roles(self) -> list[Role]:
        return self.role_repository.get_all()

    # User-Role-related methods
    def get_roles_by_user_id(self, user_id: int) -> list[Role]:
        return self.user_role_repository.get_roles_by_user_id(user_id)

    def user_has_role(self, user_id: int, role_id: int) -> bool:
        return self.user_role_repository.user_has_role(user_id, role_id)

    # Role-Permission-related methods

    def get_permissions_by_role_id(self, role_id: int) -> list[Permission]:
        return self.role_permission_repository.get_permissions_by_role_id(role_id)

    def role_has_permission(self, role_id: int, permission_id: int) -> bool:
        return self.role_permission_repository.role_has_permission(
            role_id, permission_id
        )

    def assign_permissions(self, role_id: int, permission_ids: list[int]) -> None:
        self.get_role_by_id(role_id)

        ids = set(permission_ids)  # removes duplicates

        existing = self.permission_repository.get_existing_ids(list(ids))
        missing = ids - existing
        if missing:
            raise NotFoundError("Permission", "id", f"{sorted(missing)}")

        self.role_repository.assign_permissions(role_id, list(ids))

    def assign_roles(self, user_id: int, roles_ids: list[int]) -> None:
        self.get_user_by_id(user_id)

        ids = set(roles_ids)  # removes duplicates

        existing = self.role_repository.get_existing_ids(list(ids))
        missing = ids - existing
        if missing:
            raise NotFoundError("Role", "id", f"{sorted(missing)}")

        self.user_repository.assign_roles(user_id, list(ids))
