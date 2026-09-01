from app.core.permisions import PermissionEnum, has_permission
from app.exceptions.exceptions import ForbiddenError
from app.models.permission import Permission
from app.models.user import User
from app.repositories.permision_repository import PermissionRepository


class PermissionService:
    def __init__(self, permission_repository: PermissionRepository):
        self.permission_repository = permission_repository

    def get_by_id(self, permission_id: int, current_user: User) -> Permission | None:
        if not has_permission(current_user, PermissionEnum.PERMISSIONS_READ):
            raise ForbiddenError("You dont have permission to read permissions.")
        return self.permission_repository.get_by_id(permission_id)

    def get_by_name(self, name: str, current_user: User) -> Permission | None:
        if not has_permission(current_user, PermissionEnum.PERMISSIONS_READ):
            raise ForbiddenError("You dont have permission to read permissions.")
        return self.permission_repository.get_by_name(name)

    def get_all(self, current_user: User) -> list[Permission]:
        if not has_permission(current_user, PermissionEnum.PERMISSIONS_READ):
            raise ForbiddenError("You dont have permission to read permissions.")
        return self.permission_repository.get_all()
