from enum import StrEnum

from app.models.user import User


class PermissionEnum(StrEnum):
    """
    # TODO: Refactor permissions to be more organized and clear.
    Order permissions by resource and CRUD operations (Create, Read, Update, Delete) for better organization.
    Naming SQL permissions in the format of resource:operation (e.g., users:create, roles:read) for clarity.
    Naming for key by service logic in the format of resource_operation (e.g., USERS_CREATE, ROLES_READ) for consistency.
    """

    # users
    USERS_CREATE = "users:create"
    USERS_READ = "users:read"
    USERS_UPDATE = "users:update"
    USERS_DELETE = "users:delete"
    # roles
    ROLES_CREATE = "roles:create"
    ROLES_READ = "roles:read"
    ROLES_UPDATE = "roles:update"
    ROLES_DELETE = "roles:delete"
    # user_roles
    USER_ROLES_CREATE = "user_roles:create"
    USER_ROLES_READ = "user_roles:read"
    USER_ROLES_UPDATE = "user_roles:update"
    USER_ROLES_DELETE = "user_roles:delete"
    # role_permissions
    ROLE_PERMISSIONS_CREATE = "role_permissions:create"
    ROLE_PERMISSIONS_READ = "role_permissions:read"
    ROLE_PERMISSIONS_UPDATE = "role_permissions:update"
    ROLE_PERMISSIONS_DELETE = "role_permissions:delete"
    # permissions
    PERMISSIONS_READ = "permissions:read"
    # counters_update
    COUNTERS_UPDATE_CREATE = "counters_update:create"
    COUNTERS_UPDATE_READ = "counters_update:read"
    COUNTERS_UPDATE_UPDATE = "counters_update:update"
    COUNTERS_UPDATE_DELETE = "counters_update:delete"


def has_permission(user: User, permission: PermissionEnum) -> bool:
    if user.is_admin:
        return True

    # return permission in user_permissions(user)
    return False  # Placeholder for actual permission checking logic
