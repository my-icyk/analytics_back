from app.core.permisions import PermissionEnum, has_permission
from app.exceptions.exceptions import AlreadyExistsError, ForbiddenError
from app.models.role import Role
from app.models.user import User
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.repositories.user_role_repository import UserRoleRepository


class UserRoleService:
    def __init__(
        self,
        user_role_repository: UserRoleRepository,
        role_repository: RoleRepository,
        user_repository: UserRepository,
    ):
        self.user_role_repository = user_role_repository
        self.role_repository = role_repository
        self.user_repository = user_repository

    def assign(self, user_id: int, role_id: int, current_user: User) -> None:
        if not has_permission(current_user, PermissionEnum.USER_ROLES_CREATE):
            raise ForbiddenError("You don't have permission to assign roles.")

        self.user_repository.get_by_id(user_id)
        self.role_repository.get_by_id(role_id)

        if self.user_role_repository.exists(user_id, role_id):
            raise AlreadyExistsError(
                entity="UserRole",
                field="user_id and role_id",
                value=f"{user_id} and {role_id}",
            )

        self.user_role_repository.create(user_id, role_id)

    def remove(self, user_id: int, role_id: int, current_user: User) -> None:
        if not has_permission(current_user, PermissionEnum.USER_ROLES_DELETE):
            raise ForbiddenError("You don't have permission to remove roles.")
        # TODO: for now i will not check , need to implement smth else
        # if not self.user_role_repository.exists(user_id, role_id):
        #     raise NotFoundError(
        #         entity="UserRole",
        #         field="user_id and role_id",
        #         value=f"{user_id} and {role_id}",
        #     )

        self.user_role_repository.delete(user_id, role_id)

    def get_roles_by_user_id(self, user_id: int, current_user: User) -> list[Role]:
        if not has_permission(current_user, PermissionEnum.USER_ROLES_READ):
            raise ForbiddenError("You don't have permission to view this user's roles.")

        self.user_repository.get_by_id(user_id)
        return self.user_role_repository.get_roles_by_user_id(user_id)
