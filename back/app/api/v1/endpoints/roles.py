from fastapi import APIRouter, Depends, status

from app.api.deps import (
    get_role_permission_service,
    require_permission,
)
from app.api.v1.schemas.auth import AssignRolePermissionsRequest
from app.api.v1.schemas.common import IdResponse
from app.core.permisions import PermissionEnum
from app.schemas.permission_schema import PermissionRead
from app.schemas.role_schema import RoleCreate, RoleListItem, RoleUpdate
from app.services.role_permission_service import RolePermissionService

router = APIRouter(prefix="/roles", tags=["roles"])


# NEED TO REFACTOR TO GET ALL ROLES
@router.get("", response_model=list[RoleListItem])
def get_roles(
    service: RolePermissionService = Depends(get_role_permission_service),
    _=Depends(require_permission(PermissionEnum.ROLE_READ)),
):
    items = service.get_roles()
    return items


@router.get("/{role_id}", response_model=RoleListItem)
def get_role(
    role_id: int,
    service: RolePermissionService = Depends(get_role_permission_service),
    _=Depends(require_permission(PermissionEnum.ROLE_READ)),
):
    return service.get_role_by_id(role_id)


@router.post("", response_model=IdResponse)
def create(
    payload: RoleCreate,
    service: RolePermissionService = Depends(get_role_permission_service),
    _=Depends(require_permission(PermissionEnum.ROLE_CREATE)),
):
    role_id = service.create_role(payload.name, payload.description)
    return IdResponse(id=role_id)


@router.put("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def update(
    role_id: int,
    payload: RoleUpdate,
    service: RolePermissionService = Depends(get_role_permission_service),
    _=Depends(require_permission(PermissionEnum.ROLE_UPDATE)),
):
    service.update_role(role_id, payload.name, payload.description)


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    role_id: int,
    service: RolePermissionService = Depends(get_role_permission_service),
    _=Depends(require_permission(PermissionEnum.ROLE_DELETE)),
):
    service.delete_role(role_id)


@router.get("/{role_id}/permissions", response_model=list[PermissionRead])
def get_permissions_by_role_id(
    role_id: int,
    service: RolePermissionService = Depends(get_role_permission_service),
    _=Depends(require_permission(PermissionEnum.ROLE_PERMISSION_READ)),
):
    return service.get_permissions_by_role_id(role_id)


@router.put("/{role_id}/permissions", status_code=status.HTTP_204_NO_CONTENT)
def assign_role_permissions(
    role_id: int,
    payload: AssignRolePermissionsRequest,
    service: RolePermissionService = Depends(get_role_permission_service),
    _=Depends(require_permission(PermissionEnum.AUTH_ROLE_ASSIGN_PERMISSIONS)),
) -> None:
    service.assign_permissions(role_id, payload.permission_ids)
