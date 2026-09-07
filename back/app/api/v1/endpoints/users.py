from fastapi import APIRouter, Depends, status

from app.api.deps import (
    get_auth_service,
    get_current_user,
    get_my_user_info,
    get_user_service,
)
from app.models.user import User
from app.schemas.user_schemas import MyUser, UserCreate, UserRead, UserUpdate
from app.services.auth_service import AuthService
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserRead])
def get_all_users(
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_all_users(current_user)


@router.get("/me", response_model=MyUser)
def me(current_user: MyUser = Depends(get_my_user_info)):
    return current_user


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    service: AuthService = Depends(get_auth_service),
    current_user: User | None = Depends(get_current_user),
):

    return service.create_user(payload, current_user=current_user)


@router.get("/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_user(user_id, current_user)


@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    payload: UserUpdate,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    return service.update_user(
        user_id, payload.username, payload.is_admin, current_user
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    service.delete_user(user_id, current_user)
    return None
