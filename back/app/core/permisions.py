from enum import StrEnum

from app.domains.user import User
from app.schemas.user_schemas import MyUser


class PermissionEnum(StrEnum):
    """
    # TODO: Refactor permissions to be more organized and clear.
    Order permissions by resource and CRUD operations (Create, Read, Update, Delete) for better organization.
    Naming SQL permissions in the format of resource:operation (e.g., users:create, roles:read) for clarity.
    Naming for key by service logic in the format of resource_operation (e.g., USERS_CREATE, ROLES_READ) for consistency.
    """

    SYSTEM_HEALTH_READ = "system:health:read"
    # users
    USER_CREATE = "user:create"
    USER_READ = "user:read"
    USER_UPDATE = "user:update"
    USER_DELETE = "user:delete"
    # roles
    ROLE_CREATE = "role:create"
    ROLE_READ = "role:read"
    ROLE_UPDATE = "role:update"
    ROLE_DELETE = "role:delete"
    # user_roles
    USER_ROLE_ASSIGN = "user_role:assign"
    USER_ROLE_REVOKE = "user_role:revoke"
    USER_ROLE_READ = "user_role:read"
    # role_permissions
    ROLE_PERMISSION_ASSIGN = "role_permission:assign"
    ROLE_PERMISSION_REVOKE = "role_permission:revoke"
    ROLE_PERMISSION_READ = "role_permission:read"
    # permissions
    PERMISSION_READ = "permission:read"
    # counters_update
    COUNTER_UPDATE_CREATE = "counter_update:create"
    COUNTER_UPDATE_READ = "counter_update:read"
    COUNTER_UPDATE_UPDATE = "counter_update:update"
    COUNTER_UPDATE_DELETE = "counter_update:delete"
    # specific permissions
    PRODUCT_PRICES_READ = "product_prices:read"
    MANAGE_ADMIN_RIGHTS = "user:manage_admin"

    FINANCE_DIVISION_CREATE = "finance:division:create"
    FINANCE_DIVISION_READ = "finance:division:read"
    FINANCE_DIVISION_UPDATE = "finance:division:update"
    FINANCE_DIVISION_DELETE = "finance:division:delete"

    FINANCE_GROUP_CREATE = "finance:group:create"
    FINANCE_GROUP_READ = "finance:group:read"
    FINANCE_GROUP_UPDATE = "finance:group:update"
    FINANCE_GROUP_DELETE = "finance:group:delete"

    FINANCE_RULE_CREATE = "finance:rule:create"
    FINANCE_RULE_READ = "finance:rule:read"
    FINANCE_RULE_UPDATE = "finance:rule:update"
    FINANCE_RULE_DELETE = "finance:rule:delete"

    FINANCE_RULE_TARGET_CREATE = "finance:rule_target:create"
    FINANCE_RULE_TARGET_READ = "finance:rule_target:read"
    FINANCE_RULE_TARGET_UPDATE = "finance:rule_target:update"
    FINANCE_RULE_TARGET_DELETE = "finance:rule_target:delete"


def has_permission(user: User, permission: PermissionEnum) -> bool:
    if user.is_admin:
        return True

    # return permission in user_permissions(user)
    return False  # Placeholder for actual permission checking logic


# TODO: NEED HARD REWORDK THAT
def user_has_permission(user_info: MyUser, permission: PermissionEnum) -> bool:
    if user_info.user.is_admin:
        return True

    if permission in user_info.permissions:
        return True
    return False
