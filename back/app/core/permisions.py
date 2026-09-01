from enum import StrEnum

from app.models.user import User


class Permission(StrEnum):
    USERS_CREATE = "users:create"
    USERS_READ = "users:read"
    USERS_UPDATE = "users:update"
    USERS_DELETE = "users:delete"

    ROLES_CREATE = "roles:create"
    ROLES_READ = "roles:read"
    ROLES_UPDATE = "roles:update"
    ROLES_DELETE = "roles:delete"

    USER_ROLES_CREATE = "user_roles:create"
    USER_ROLES_READ = "user_roles:read"
    USER_ROLES_UPDATE = "user_roles:update"
    USER_ROLES_DELETE = "user_roles:delete"

    PERMISSIONS_READ = "permissions:read"
    PERMISSIONS_ASSIGN = "permissions:assign"
    ROLE_ASSIGN = "role:assign"


def has_permission(user: User, permission: Permission) -> bool:
    if user.is_admin:
        return True

    # return permission in user_permissions(user)
    return False  # Placeholder for actual permission checking logic
