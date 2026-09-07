from fastapi import APIRouter, Depends

from app.api.deps import get_current_user, get_role_service
from app.models.user import User
from app.schemas.role_schema import RoleCreate, RoleRead
from app.schemas.user_schemas import UserRead
from app.services.role_service import RoleService

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("/", response_model=list[RoleRead])
def get_all_roles(
    service: RoleService = Depends(get_role_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_all_roles(current_user)


@router.post("/", response_model=RoleRead)
def create_role(
    role_data: RoleCreate,
    service: RoleService = Depends(get_role_service),
    current_user: User = Depends(get_current_user),
):
    return service.create_role(role_data.name, role_data.description, current_user)


@router.get("/{role_id}", response_model=RoleRead)
def get_role(
    role_id: int,
    service: RoleService = Depends(get_role_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_role(role_id, current_user)


@router.get("/{user_id}/roles", response_model=list[RoleRead])
def get_roles_by_user_id(
    user_id: int,
    service: RoleService = Depends(get_role_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_roles_by_user_id(user_id, current_user)


@router.get("/{role_id}/users", response_model=list[UserRead])
def get_users_by_role_id(
    role_id: int,
    service: RoleService = Depends(get_role_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_users_by_role_id(role_id, current_user)
