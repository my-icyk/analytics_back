from fastapi import APIRouter, Depends

from app.api.deps import (
    get_role_permission_service,
    require_permission,
)
from app.core.permisions import PermissionEnum
from app.schemas.permission_schema import PermissionRead
from app.services.auth.role_permission_service import RolePermissionService

router = APIRouter()


@router.get("", response_model=list[PermissionRead])
def get_permissions(
    service: RolePermissionService = Depends(get_role_permission_service),
    _=Depends(require_permission(PermissionEnum.PERMISSION_READ)),
):
    return service.get_permissions()
