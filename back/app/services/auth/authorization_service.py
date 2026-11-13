from app.core import PermissionEnum
from app.db.models.auth import User
from app.exceptions.exceptions import ForbiddenError
from app.repositories.auth import AuthorizationRepository


class AuthorizationService:
    def __init__(
        self,
        authorization_repo: AuthorizationRepository,
    ):
        self.authorization_repo = authorization_repo

    def user_has_permission(self, user: User, permission: PermissionEnum) -> bool:
        if user.is_admin:
            return True
        return self.authorization_repo.user_has_permission(user.id, permission.value)

    def require_permission(self, user: User, permission: PermissionEnum) -> None:
        if not self.user_has_permission(user, permission):
            raise ForbiddenError(f"Missing permission: {permission.value}")
