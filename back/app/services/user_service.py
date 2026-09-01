from app.core.permisions import PermissionEnum, has_permission
from app.exceptions.exceptions import ForbiddenError, NotFoundError, UserNotFoundError
from app.models.role import Role
from app.models.user import User
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user(self, user_id: int, current_user: User) -> User:
        if not has_permission(current_user, PermissionEnum.USERS_READ):
            raise ForbiddenError("You dont have permission to access this user's data.")
        user = self.user_repository.get_by_id(user_id)

        if user is None:
            raise UserNotFoundError(user_id)

        return user

    def assign_role_to_user(
        self, user_id: int, role_id: int, current_user: User
    ) -> None:
        if not has_permission(current_user, PermissionEnum.USER_ROLES_CREATE):
            raise ForbiddenError("You dont have permission to assign a role to a user.")
        return self.role_repository.create(user_id, role_id)

    def remove_role_from_user(
        self, user_id: int, role_id: int, current_user: User
    ) -> None:
        if not has_permission(current_user, PermissionEnum.USER_ROLES_DELETE):
            raise ForbiddenError(
                "You dont have permission to remove a role from a user."
            )
        self.role_repository.delete(user_id, role_id)

    def get_roles_by_user_id(self, user_id: int, current_user: User) -> list[Role]:
        if not has_permission(current_user, PermissionEnum.USER_ROLES_READ):
            raise ForbiddenError(
                "You dont have permission to access this user's roles."
            )
        roles = self.role_repository.get_roles_by_user_id(user_id)
        if roles is None:
            raise NotFoundError("Roles", "user_id", user_id)
        return self.role_repository.get_roles_by_user_id(user_id)
