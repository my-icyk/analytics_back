from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.permisions import PermissionEnum
from app.db.database import get_db
from app.repositories.authentication_repository import AuthenticationRepository
from app.repositories.authorization_repository import AuthorizationRepository
from app.repositories.counter_update_repository import CounterUpdateRepository
from app.repositories.division_repository import DivisionRepository
from app.repositories.group_repository import GroupRepository
from app.repositories.group_rule_repository import GroupRuleRepository
from app.repositories.group_rule_target_repository import GroupRuleTargetRepository
from app.repositories.group_type_repository import GroupTypeRepository
from app.repositories.permision_repository import PermissionRepository
from app.repositories.role_permission_repository import RolePermissionRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.specific_repository import SpecificRepository
from app.repositories.user_repository import UserRepository
from app.repositories.user_role_repository import UserRoleRepository
from app.services.authentication_service import AuthenticationService
from app.services.authorization_service import AuthorizationService
from app.services.counter_update_service import CounterUpdateService
from app.services.finance_group_service import FinanceGroupService
from app.services.finance_rule_service import FinanceRuleService
from app.services.role_permission_service import RolePermissionService
from app.services.specific_service import SpecificService
from app.services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token", auto_error=False)


# TODO: WTF HERE IS HAPPENDS
def get_specific_repository(db: Session = Depends(get_db)) -> SpecificRepository:
    return SpecificRepository(db)


def get_auth_repository(db: Session = Depends(get_db)) -> AuthenticationRepository:
    return AuthenticationRepository(db)


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_role_repository(db: Session = Depends(get_db)) -> RoleRepository:
    return RoleRepository(db)


def get_user_role_repository(db: Session = Depends(get_db)) -> UserRoleRepository:
    return UserRoleRepository(db)


def get_permission_repository(db: Session = Depends(get_db)) -> PermissionRepository:
    return PermissionRepository(db)


def get_authorization_repository(
    db: Session = Depends(get_db),
) -> AuthorizationRepository:
    return AuthorizationRepository(db)


def get_counter_update_repository(
    db: Session = Depends(get_db),
) -> CounterUpdateRepository:
    return CounterUpdateRepository(db)


def get_role_permission_repository(
    db: Session = Depends(get_db),
) -> RolePermissionRepository:
    return RolePermissionRepository(db)


def get_division_repository(db: Session = Depends(get_db)) -> DivisionRepository:
    return DivisionRepository(db)


def get_group_repository(db: Session = Depends(get_db)) -> GroupRepository:
    return GroupRepository(db)


def get_group_rule_repository(db: Session = Depends(get_db)) -> GroupRuleRepository:
    return GroupRuleRepository(db)


def get_group_rule_target_repository(
    db: Session = Depends(get_db),
) -> GroupRuleTargetRepository:
    return GroupRuleTargetRepository(db)


def get_group_type_repository(db: Session = Depends(get_db)) -> GroupTypeRepository:
    return GroupTypeRepository(db)


# Services
def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository),
    auth_repo: AuthenticationRepository = Depends(get_auth_repository),
) -> AuthenticationService:
    return AuthenticationService(user_repo, auth_repo)


def get_specific_service(
    specific_repo: SpecificRepository = Depends(get_specific_repository),
) -> SpecificService:
    return SpecificService(specific_repo)


def get_user_service(
    user_repo: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(user_repo)


def get_role_permission_service(
    role_repository: RoleRepository = Depends(get_role_repository),
    permission_repository: PermissionRepository = Depends(get_permission_repository),
    role_permission_repository: RolePermissionRepository = Depends(
        get_role_permission_repository
    ),
    user_role_repository: UserRoleRepository = Depends(get_user_role_repository),
) -> RolePermissionService:
    return RolePermissionService(
        role_repository=role_repository,
        permission_repository=permission_repository,
        role_permission_repository=role_permission_repository,
        user_role_repository=user_role_repository,
    )


def get_counter_update_service(
    counter_update_repo: CounterUpdateRepository = Depends(
        get_counter_update_repository
    ),
) -> CounterUpdateService:
    return CounterUpdateService(counter_update_repo)


def get_authorization_service(
    authorization_repo: AuthorizationRepository = Depends(get_authorization_repository),
) -> AuthorizationService:
    return AuthorizationService(
        authorization_repo=authorization_repo,
    )


# requirements
def require_permission(permission: PermissionEnum):
    def permission_dependency(
        token: str | None = Depends(oauth2_scheme),
        auth_service: AuthenticationService = Depends(get_auth_service),
        authorization_service: AuthorizationService = Depends(
            get_authorization_service
        ),
    ) -> int:
        if token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
            )
        user_id = auth_service.authenticate_user(token)

        authorization_service.require_permission(
            user_id,
            permission,
        )
        return user_id

    return permission_dependency


def get_current_user_id(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthenticationService = Depends(get_auth_service),
) -> int:
    return auth_service.authenticate_user(token)


def get_finance_group_service(
    group_type_repository: GroupTypeRepository = Depends(get_group_type_repository),
    division_repository: DivisionRepository = Depends(get_division_repository),
    group_repository: GroupRepository = Depends(get_group_repository),
    group_rule_repository: GroupRuleRepository = Depends(get_group_rule_repository),
) -> FinanceGroupService:
    return FinanceGroupService(
        group_type_repository=group_type_repository,
        division_repository=division_repository,
        group_repository=group_repository,
        group_rule_repository=group_rule_repository,
    )


def get_finance_rule_service(
    group_repository: GroupRepository = Depends(get_group_repository),
    group_rule_repository: GroupRuleRepository = Depends(get_group_rule_repository),
    group_rule_target_repository: GroupRuleTargetRepository = Depends(
        get_group_rule_target_repository
    ),
) -> FinanceRuleService:
    return FinanceRuleService(
        group_repository=group_repository,
        group_rule_repository=group_rule_repository,
        group_rule_target_repository=group_rule_target_repository,
    )
