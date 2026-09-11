from fastapi import APIRouter, Depends, status

from app.api.deps import (
    get_role_permission_service,
    require_permission,
)
from app.core.permisions import PermissionEnum
from app.schemas.permission_schema import PermissionRead
from app.schemas.role_schema import RoleCreate, RoleRead, RoleUpdate
from app.services.role_permission_service import RolePermissionService

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("", response_model=list[RoleRead])
def get_roles(
    service: RolePermissionService = Depends(get_role_permission_service),
    _=Depends(require_permission(PermissionEnum.ROLE_READ)),
):
    return service.get_roles()


@router.get("/{role_id}", response_model=RoleRead)
def get_role(
    role_id: int,
    service: RolePermissionService = Depends(get_role_permission_service),
    _=Depends(require_permission(PermissionEnum.ROLE_READ)),
):
    return service.get_role_by_id(role_id)


@router.post("", response_model=RoleRead)
def create(
    payload: RoleCreate,
    service: RolePermissionService = Depends(get_role_permission_service),
    _=Depends(require_permission(PermissionEnum.ROLE_CREATE)),
):
    return service.create_role(payload.name, payload.description)


@router.put("/{role_id}", response_model=RoleRead)
def update(
    role_id: int,
    payload: RoleUpdate,
    service: RolePermissionService = Depends(get_role_permission_service),
    _=Depends(require_permission(PermissionEnum.ROLE_UPDATE)),
):
    return service.update_role(role_id, payload.name, payload.description)


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    role_id: int,
    service: RolePermissionService = Depends(get_role_permission_service),
    _=Depends(require_permission(PermissionEnum.ROLE_DELETE)),
):
    service.delete_role(role_id)


@router.post(
    "/{role_id}/permissions/{permission_id}", status_code=status.HTTP_204_NO_CONTENT
)
def assign_permission_to_role(
    role_id: int,
    permission_id: int,
    service: RolePermissionService = Depends(get_role_permission_service),
    _: int = Depends(require_permission(PermissionEnum.ROLE_PERMISSION_ASSIGN)),
):
    service.assign_permission_to_role(role_id, permission_id)


@router.delete(
    "/{role_id}/permissions/{permission_id}", status_code=status.HTTP_204_NO_CONTENT
)
def revoke_permission_from_role(
    role_id: int,
    permission_id: int,
    service: RolePermissionService = Depends(get_role_permission_service),
    _: int = Depends(require_permission(PermissionEnum.ROLE_PERMISSION_REVOKE)),
):
    service.revoke_permission_from_role(role_id, permission_id)


@router.get("/{role_id}/permissions", response_model=list[PermissionRead])
def get_permissions_by_role_id(
    role_id: int,
    service: RolePermissionService = Depends(get_role_permission_service),
    _: int = Depends(require_permission(PermissionEnum.ROLE_PERMISSION_READ)),
):
    return service.get_permissions_by_role_id(role_id)
