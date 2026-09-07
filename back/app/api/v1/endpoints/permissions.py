from fastapi import APIRouter, Depends

from app.api.deps import get_current_user, get_permission_service
from app.models.user import User
from app.schemas.permission_schema import PermissionRead
from app.services.permission_service import PermissionService

router = APIRouter(prefix="/permissions", tags=["permissions"])


@router.get("/", response_model=list[PermissionRead])
def get_permissions(
    service: PermissionService = Depends(get_permission_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_all(current_user)


@router.get("/{permission_id}", response_model=PermissionRead)
def get_permission(
    permission_id: int,
    service: PermissionService = Depends(get_permission_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_by_id(permission_id, current_user)
