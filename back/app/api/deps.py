from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.database import get_db
from app.models.user import User
from app.repositories.auth_repository import AuthRepository
from app.repositories.permision_repository import PermissionRepository
from app.repositories.role_permission_repository import RolePermissionRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.repositories.user_role_repository import UserRoleRepository
from app.schemas.user_schemas import MyUser, UserRead
from app.services.auth_service import AuthService
from app.services.permission_service import PermissionService
from app.services.role_permission_service import RolePermissionService
from app.services.role_service import RoleService
from app.services.user_roles_service import UserRoleService
from app.services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token", auto_error=False)


# TODO: WTF HERE IS HAPPENDS


def get_auth_repository(db: Session = Depends(get_db)) -> AuthRepository:
    return AuthRepository(db)


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_role_repository(db: Session = Depends(get_db)) -> RoleRepository:
    return RoleRepository(db)


def get_user_role_repository(db: Session = Depends(get_db)) -> UserRoleRepository:
    return UserRoleRepository(db)


def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository),
    auth_repo: AuthRepository = Depends(get_auth_repository),
) -> AuthService:
    return AuthService(user_repo, auth_repo)


def get_user_role_service(
    user_role_repo: UserRoleRepository = Depends(get_user_role_repository),
    role_repo: RoleRepository = Depends(get_role_repository),
    user_repo: UserRepository = Depends(get_user_repository),
) -> UserRoleService:
    return UserRoleService(user_role_repo, role_repo, user_repo)


def get_permission_repository(db: Session = Depends(get_db)) -> PermissionRepository:
    return PermissionRepository(db)


def get_role_permission_repository(
    db: Session = Depends(get_db),
) -> RolePermissionRepository:
    return RolePermissionRepository(db)


def get_role_permission_service(
    role_repository: RoleRepository = Depends(get_role_repository),
    permission_repo: PermissionRepository = Depends(get_permission_repository),
    role_permission_repo: RolePermissionRepository = Depends(
        get_role_permission_repository
    ),
) -> RolePermissionService:
    return RolePermissionService(
        role_repository=role_repository,
        permission_repository=permission_repo,
        role_permission_repository=role_permission_repo,
    )


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))


def get_role_service(db: Session = Depends(get_db)) -> RoleService:
    return RoleService(RoleRepository(db))


def get_permission_service(db: Session = Depends(get_db)) -> PermissionService:
    return PermissionService(PermissionRepository(db))


def get_current_user(
    token: str | None = Depends(oauth2_scheme),
    user_repo: UserRepository = Depends(get_user_repository),
) -> User:
    # todo: add caching for user retrieval to reduce db hits
    # todo: add token expiration check and refresh mechanism
    # todo: exception in other ways, maybe use a custom exception class for better error handling
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # todo probabil nu trebuie aici
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id: int = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    user = user_repo.get_by_id(user_id)
    if user is None:
        raise credentials_exception

    return user


# TODO: need to chenge the logic of this function, because it is not good to return the user with permissions in this way, maybe we need to create a new model for this
def get_my_user_info(
    token: str | None = Depends(oauth2_scheme),
    user_repo: UserRepository = Depends(get_user_repository),
) -> MyUser:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id: int = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = user_repo.get_by_id(user_id)
    if user is None:
        raise credentials_exception
    permissions = user_repo.get_user_permissions(user_id)

    return MyUser(
        user=UserRead(id=user.id, username=user.username, is_admin=user.is_admin),
        permissions=permissions,
    )
