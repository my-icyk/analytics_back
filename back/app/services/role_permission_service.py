from sqlalchemy.orm import Session

from app.db.models.auth import Permission, Role, User
from app.exceptions.exceptions import (
    AlreadyExistsError,
    DeleteProtectedError,
    NotFoundError,
)
from app.repositories.auth import UserRepository
from app.repositories.auth.permision_repository import PermissionRepository
from app.repositories.auth.role_permission_repository import RolePermissionRepository
from app.repositories.auth.role_repository import RoleRepository
from app.repositories.auth.user_role_repository import UserRoleRepository
from app.services.common import WriteService


class RolePermissionService(WriteService):
    def __init__(
        self,
        session: Session,
        role_repository: RoleRepository,
        permission_repository: PermissionRepository,
        role_permission_repository: RolePermissionRepository,
        user_role_repository: UserRoleRepository,
        user_repository: UserRepository,
    ) -> None:
        super().__init__(session)
        self.role_repository = role_repository
        self.permission_repository = permission_repository
        self.role_permission_repository = role_permission_repository
        self.user_role_repository = user_role_repository
        self.user_repository = user_repository

    def get_role_by_id(self, role_id: int) -> Role:
        role = self.role_repository.get_by_id(role_id)
        if role is None:
            raise NotFoundError("Role", "role_id", str(role_id))
        return role

    def get_user_by_id(self, user_id: int) -> User:
        user = self.user_repository.get_by_id(user_id)
        if user is None:
            raise NotFoundError("User", "user_id", str(user_id))
        return user

    def get_roles(self) -> list[Role]:
        return self.role_repository.get_all()

    def get_permissions(self) -> list[Permission]:
        return self.permission_repository.get_all()

    def get_roles_by_user_id(self, user_id: int) -> list[Role]:
        return self.user_role_repository.get_roles_by_user_id(user_id)

    def get_permissions_by_user_id(self, user_id: int) -> list[Permission]:
        return self.role_permission_repository.get_permissions_by_user_id(user_id)

    def get_permissions_by_role_id(self, role_id: int) -> list[Permission]:
        return self.role_permission_repository.get_permissions_by_role_id(role_id)

    def user_has_role(self, user_id: int, role_id: int) -> bool:
        return self.user_role_repository.user_has_role(user_id, role_id)

    def role_has_permission(self, role_id: int, permission_id: int) -> bool:
        return self.role_permission_repository.role_has_permission(
            role_id, permission_id
        )

    def create_role(self, role_name: str, role_description: str | None = None) -> int:
        with self._write():
            if self.role_repository.get_by_name(role_name) is not None:
                raise AlreadyExistsError("Role", "role_name", role_name)

            role_id = self.role_repository.create(role_name, role_description)

        return role_id

    def update_role(
        self, role_id: int, role_name: str, role_description: str | None = None
    ) -> None:
        with self._write():
            role = self.get_role_by_id(role_id)
            role.name = role_name
            role.description = role_description

    def delete_role(self, role_id: int) -> None:
        with self._write():
            role = self.get_role_by_id(role_id)
            if role.users_count > 0:
                raise DeleteProtectedError(
                    entity="Role",
                    reason=f"Role with id {role_id} has associated ({role.users_count}) users",
                )

            self.role_repository.delete(role_id)

    def assign_permissions(self, role_id: int, permission_ids: list[int]) -> None:
        with self._write():
            self.get_role_by_id(role_id)

            ids = sorted(set(permission_ids))
            existing = self.permission_repository.get_existing_ids(ids)
            missing = set(ids) - existing
            if missing:
                raise NotFoundError("Permission", "id", str(sorted(missing)))

            self.role_repository.assign_permissions(role_id, ids)

    def assign_roles(self, user_id: int, roles_ids: list[int]) -> None:
        with self._write():
            self.get_user_by_id(user_id)

            ids = sorted(set(roles_ids))
            existing = self.role_repository.get_existing_ids(ids)
            missing = set(ids) - existing
            if missing:
                raise NotFoundError("Role", "id", str(sorted(missing)))

            self.user_role_repository.assign_roles(user_id, ids)
