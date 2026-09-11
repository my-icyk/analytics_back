from fastapi import APIRouter, Depends, status

from app.api.deps import (
    get_role_permission_service,
    get_user_service,
    require_permission,
)
from app.api.v1.schemas.users_schema import UserCreate, UserRead, UserUpdate
from app.core.permisions import PermissionEnum
from app.schemas.role_schema import RoleRead
from app.services.role_permission_service import RolePermissionService
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserRead])
def get_all_users(
    service: UserService = Depends(get_user_service),
    _: int = Depends(require_permission(PermissionEnum.USER_READ)),
):
    return service.get_all_users()


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    service: UserService = Depends(get_user_service),
    _: int = Depends(require_permission(PermissionEnum.USER_CREATE)),
):

    return service.create_user(
        payload.username,
        payload.password,
    )


@router.get("/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    _: int = Depends(require_permission(PermissionEnum.USER_READ)),
):
    return service.get_user(user_id)


@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    payload: UserUpdate,
    service: UserService = Depends(get_user_service),
    _: int = Depends(require_permission(PermissionEnum.USER_UPDATE)),
):
    return service.update_user(user_id, payload.username)


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


@router.post("/{user_id}/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def assign_role_to_user(
    user_id: int,
    role_id: int,
    service: RolePermissionService = Depends(get_role_permission_service),
    _: int = Depends(require_permission(PermissionEnum.USER_ROLE_ASSIGN)),
):
    service.assign_role_to_user(user_id, role_id)


@router.delete("/{user_id}/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def revoke_role_from_user(
    user_id: int,
    role_id: int,
    service: RolePermissionService = Depends(get_role_permission_service),
    _: int = Depends(require_permission(PermissionEnum.USER_ROLE_REVOKE)),
):
    service.revoke_role_from_user(user_id, role_id)
