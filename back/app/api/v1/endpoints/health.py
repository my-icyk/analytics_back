from fastapi import APIRouter, Depends

from app.api.deps import require_permission
from app.core.permisions import PermissionEnum

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/api")
def health():
    return {"status": "success", "message": "api is working"}


@router.get("/protected")
def protected_health(
    _=Depends(require_permission(PermissionEnum.SYSTEM_HEALTH_READ)),
):
    return {"status": "success", "message": "api is working"}
