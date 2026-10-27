from fastapi import APIRouter, Depends, status

from app.api.deps import (
    get_current_user_id,
    get_role_permission_service,
    get_user_service,
    require_permission,
)
from app.api.v1.schemas.auth import AssignUserRolesRequest
from app.api.v1.schemas.user import MyUser, UserCreate, UserRead, UserUpdate
from app.core.permisions import PermissionEnum
from app.repositories.base import LookupResponse
from app.schemas.role_schema import RoleRead
from app.services.role_permission_service import RolePermissionService
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=MyUser)
def get_me(
    user_service: UserService = Depends(get_user_service),
    role_permission_service: RolePermissionService = Depends(
        get_role_permission_service
    ),
    user_id: int = Depends(get_current_user_id),
):
    user = user_service.get_user(user_id)
    # TODO: De clarificat de ce nu se convertesc bine
    roles = role_permission_service.get_roles_by_user_id(user_id)
    permissions = role_permission_service.get_permissions_by_user_id(user_id)
    return MyUser(
        id=user.id,
        username=user.username,
        is_admin=user.is_admin,
        roles=[role.name for role in roles],
        permissions=[permission.name for permission in permissions],
    )


@router.get("", response_model=list[UserRead])
def get_all_users(
    service: UserService = Depends(get_user_service),
    _: int = Depends(require_permission(PermissionEnum.USER_READ)),
):

    return service.get_all_users()


@router.get("/lookup", response_model=list[LookupResponse])
def lookup_users(
    search: str,
    service: UserService = Depends(get_user_service),
    _: int = Depends(require_permission(PermissionEnum.USER_READ)),
):

    return service.lookup_users(search=search)


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    service: UserService = Depends(get_user_service),
    _: int = Depends(require_permission(PermissionEnum.USER_CREATE)),
):

    return service.create_user(
        payload.username,
        payload.password,
        payload.name,
        payload.email,
    )


@router.get("/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    _: int = Depends(require_permission(PermissionEnum.USER_READ)),
):
    return service.get_user(user_id)


@router.put("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_user(
    user_id: int,
    payload: UserUpdate,
    service: UserService = Depends(get_user_service),
    _: int = Depends(require_permission(PermissionEnum.USER_UPDATE)),
):
    service.update_user(
        user_id, payload.username, payload.email, payload.is_active, payload.name
    )


@router.patch("/users/{user_id}/grant-admin", response_model=UserRead)
def grant_admin(
    user_id: int,
    service: UserService = Depends(get_user_service),
    _: int = Depends(require_permission(PermissionEnum.MANAGE_ADMIN_RIGHTS)),
):
    return service.set_admin(user_id)


@router.patch("/users/{user_id}/revoke-admin", response_model=UserRead)
def revoke_admin(
    user_id: int,
    service: UserService = Depends(get_user_service),
    _: int = Depends(require_permission(PermissionEnum.MANAGE_ADMIN_RIGHTS)),
):
    return service.revoke_admin(user_id)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    _: int = Depends(require_permission(PermissionEnum.USER_DELETE)),
):
    service.delete_user(user_id)


@router.get("/{user_id}/roles", response_model=list[RoleRead])
def get_roles_by_user_id(
    user_id: int,
    service: RolePermissionService = Depends(get_role_permission_service),
    _=Depends(require_permission(PermissionEnum.USER_ROLE_READ)),
):
    return service.get_roles_by_user_id(user_id)


@router.put("/{user_id}/roles", status_code=status.HTTP_204_NO_CONTENT)
def assign_roles_to_user(
    user_id: int,
    payload: AssignUserRolesRequest,
    service: RolePermissionService = Depends(get_role_permission_service),
    _: int = Depends(require_permission(PermissionEnum.AUTH_USER_ASSIGN_ROLES)),
):
    service.assign_roles(user_id, payload.role_ids)
