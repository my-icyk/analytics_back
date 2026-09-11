from app.core.permisions import PermissionEnum
from app.exceptions.exceptions import ForbiddenError
from app.repositories.authorization_repository import AuthorizationRepository


class AuthorizationService:
    def __init__(
        self,
        authorization_repo: AuthorizationRepository,
    ):
        self.authorization_repo = authorization_repo

    def is_admin(self, user_id: int) -> bool:
        return self.authorization_repo.user_is_admin(user_id)

    def user_has_permission(self, user_id: int, permission: PermissionEnum) -> bool:
        if self.is_admin(user_id):
            return True
        return self.authorization_repo.user_has_permission(user_id, permission.value)

    def require_permission(self, user_id: int, permission: PermissionEnum) -> None:
        if not self.user_has_permission(user_id, permission):
            raise ForbiddenError(f"Missing permission: {permission.value}")
