from fastapi import APIRouter, Depends, status

from app.api.deps import get_current_user, get_user_role_service
from app.models.user import User
from app.schemas.role_schema import RoleRead
from app.services.user_roles_service import UserRoleService

router = APIRouter(prefix="/users/{user_id}/roles", tags=["user-roles"])


@router.get("/", response_model=list[RoleRead])
def get_roles_by_user_id(
    user_id: int,
    service: UserRoleService = Depends(get_user_role_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_roles_by_user_id(user_id, current_user)


@router.post("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def assign_role_to_user(
    user_id: int,
    role_id: int,
    service: UserRoleService = Depends(get_user_role_service),
    current_user: User = Depends(get_current_user),
) -> None:
    service.assign(user_id, role_id, current_user)


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_role_from_user(
    user_id: int,
    role_id: int,
    service: UserRoleService = Depends(get_user_role_service),
    current_user: User = Depends(get_current_user),
) -> None:
    service.remove(user_id, role_id, current_user)
