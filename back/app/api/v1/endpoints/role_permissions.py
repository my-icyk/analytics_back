from fastapi import APIRouter, Depends, status

from app.api.deps import (
    get_current_user,
    get_role_permission_service,
)
from app.models.user import User
from app.schemas.permission_schema import PermissionRead
from app.services.role_permission_service import RolePermissionService

router = APIRouter(prefix="/roles/{role_id}/permissions", tags=["role-permissions"])


@router.get("/", response_model=list[PermissionRead])
def get_permissions_by_role_id(
    role_id: int,
    service: RolePermissionService = Depends(get_role_permission_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_permissions_by_role_id(role_id, current_user)


@router.post("/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
def assign_permission_to_role(
    role_id: int,
    permission_id: int,
    service: RolePermissionService = Depends(get_role_permission_service),
    current_user: User = Depends(get_current_user),
) -> None:
    service.assign_permission_to_role(role_id, permission_id, current_user)


@router.delete("/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_permission_from_role(
    role_id: int,
    permission_id: int,
    service: RolePermissionService = Depends(get_role_permission_service),
    current_user: User = Depends(get_current_user),
) -> None:
    service.remove_permission_from_role(role_id, permission_id, current_user)
