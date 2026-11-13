from sqlalchemy.orm import Session

from app.db.models.auth import Permission, Role, User
from app.exceptions.exceptions import (
    AlreadyExistsError,
    DeleteProtectedError,
    NotFoundError,
)
from app.repositories.auth import UserRepo
from app.repositories.auth.permission_repo import PermissionRepo
from app.repositories.auth.role_permission_repo import RolePermissionRepo
from app.repositories.auth.role_repo import RoleRepo
from app.repositories.auth.user_role_repo import UserRoleRepo
from app.services.common import WriteService


class RolePermissionService(WriteService):
    def __init__(
        self,
        session: Session,
        *,
        role_repo: RoleRepo,
        permission_repo: PermissionRepo,
        role_permission_repo: RolePermissionRepo,
        user_role_repo: UserRoleRepo,
        user_repo: UserRepo,
    ) -> None:
        super().__init__(session)
        self._roles = role_repo
        self._permissions = permission_repo
        self._role_permissions = role_permission_repo
        self._user_roles = user_role_repo
        self._users = user_repo

    def get_role_by_id(self, role_id: int) -> Role:
        role = self._roles.get_by_id(role_id)
        if role is None:
            raise NotFoundError("Role", "role_id", str(role_id))
        return role

    def get_user_by_id(self, user_id: int) -> User:
        user = self._users.get_by_id(user_id)
        if user is None:
            raise NotFoundError("User", "user_id", str(user_id))
        return user

    def get_roles(self) -> list[Role]:
        return self._roles.get_all()

    def get_permissions(self) -> list[Permission]:
        return self._permissions.get_all()

    def get_roles_by_user_id(self, user_id: int) -> list[Role]:
        return self._user_roles.get_roles_by_user_id(user_id)

    def get_permissions_by_user_id(self, user_id: int) -> list[Permission]:
        return self._role_permissions.get_permissions_by_user_id(user_id)

    def get_permissions_by_role_id(self, role_id: int) -> list[Permission]:
        return self._role_permissions.get_permissions_by_role_id(role_id)

    def user_has_role(self, user_id: int, role_id: int) -> bool:
        return self._user_roles.user_has_role(user_id, role_id)

    def role_has_permission(self, role_id: int, permission_id: int) -> bool:
        return self._role_permissions.role_has_permission(role_id, permission_id)

    def create_role(self, role_name: str, role_description: str | None = None) -> int:
        with self._write():
            if self._roles.get_by_name(role_name) is not None:
                raise AlreadyExistsError("Role", "role_name", role_name)

            role_id = self._roles.create(role_name, role_description)

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

            self._roles.delete(role_id)

    def assign_permissions(self, role_id: int, permission_ids: list[int]) -> None:
        with self._write():
            self.get_role_by_id(role_id)

            ids = sorted(set(permission_ids))
            existing = self._permissions.get_existing_ids(ids)
            missing = set(ids) - existing
            if missing:
                raise NotFoundError("Permission", "id", str(sorted(missing)))

            self._roles.assign_permissions(role_id, ids)

    def assign_roles(self, user_id: int, roles_ids: list[int]) -> None:
        with self._write():
            self.get_user_by_id(user_id)

            ids = sorted(set(roles_ids))
            existing = self._roles.get_existing_ids(ids)
            missing = set(ids) - existing
            if missing:
                raise NotFoundError("Role", "id", str(sorted(missing)))

            self._user_roles.assign_roles(user_id, ids)
