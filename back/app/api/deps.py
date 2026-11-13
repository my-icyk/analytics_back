from fastapi import Depends
from fastapi.security import APIKeyCookie
from sqlalchemy.orm import Session

from app.config import get_settings
from app.core.permisions import PermissionEnum
from app.db.database import get_db
from app.db.models.auth import User
from app.repositories.analytics import ProcedureRepository
from app.repositories.auth import (
    AuthorizationRepo,
    PermissionRepo,
    RolePermissionRepo,
    RoleRepo,
    SessionRepo,
    UserRepo,
    UserRoleRepo,
)
from app.repositories.counter_update_repository import CounterUpdateRepository
from app.repositories.finance import (
    CompanyRepo,
    DepartmentRepartitionRepo,
    DepartmentRepo,
    DivisionRepo,
    GroupRepo,
    GroupRuleRepo,
    GroupRuleTargetRepo,
    GroupTypeRepo,
)
from app.repositories.snapshot_repository import SnapshotRepository
from app.repositories.specific_repository import SpecificRepository
from app.services.analytics import ProcedureService
from app.services.auth import AuthenticationService, AuthorizationService, UserService
from app.services.auth.role_permission_service import RolePermissionService
from app.services.counter_update_service import CounterUpdateService
from app.services.employees import CreditService, EmployeeService
from app.services.finance import FinanceGroupService, FinanceRuleService
from app.services.snapshot import SnapshotService
from app.services.specific_service import SpecificService

settings = get_settings()
session_cookie = APIKeyCookie(name=settings.SESSION_COOKIE_NAME, auto_error=False)


# Services
def get_auth_service(db: Session = Depends(get_db)) -> AuthenticationService:
    return AuthenticationService(db, session_repo=SessionRepo(db))


def get_specific_service(
    db: Session = Depends(get_db),
) -> SpecificService:
    return SpecificService(SpecificRepository(db))


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(
        session=db,
        user_repo=UserRepo(db),
    )


def get_role_permission_service(
    db: Session = Depends(get_db),
) -> RolePermissionService:
    return RolePermissionService(
        session=db,
        role_repo=RoleRepo(db),
        permission_repo=PermissionRepo(db),
        role_permission_repo=RolePermissionRepo(db),
        user_role_repo=UserRoleRepo(db),
        user_repo=UserRepo(db),
    )


def get_counter_update_service(
    session: Session = Depends(get_db),
) -> CounterUpdateService:
    return CounterUpdateService(CounterUpdateRepository(session))


def get_authorization_service(
    db: Session = Depends(get_db),
) -> AuthorizationService:
    return AuthorizationService(
        authorization_repo=AuthorizationRepo(db),
    )


def require_permission(permission: PermissionEnum):
    def check(
        user: User = Depends(get_current_user),
        service: AuthorizationService = Depends(get_authorization_service),
    ) -> User:
        service.require_permission(user, permission)
        return user

    return check


def get_current_user(
    token: str | None = Depends(session_cookie),
    service: AuthenticationService = Depends(get_auth_service),
) -> User:
    return service.authenticate_user(token)


def get_finance_group_service(
    session: Session = Depends(get_db),
) -> FinanceGroupService:
    return FinanceGroupService(
        session=session,
        group_type_repo=GroupTypeRepo(session),
        division_repo=DivisionRepo(session),
        group_repo=GroupRepo(session),
        group_rule_repo=GroupRuleRepo(session),
        department_repo=DepartmentRepo(session),
        department_repartition_repo=DepartmentRepartitionRepo(session),
        company_repo=CompanyRepo(session),
    )


def get_finance_rule_service(
    session: Session = Depends(get_db),
) -> FinanceRuleService:
    return FinanceRuleService(
        session=session,
        group_repo=GroupRepo(session),
        group_rule_repo=GroupRuleRepo(session),
        group_rule_target_repo=GroupRuleTargetRepo(session),
    )


def get_snapshot_service(session: Session = Depends(get_db)) -> SnapshotService:
    return SnapshotService(
        snapshot_repository=SnapshotRepository(session),
    )


def get_procedure_service(
    session: Session = Depends(get_db),
) -> ProcedureService:
    return ProcedureService(
        procedure_repository=ProcedureRepository(session),
    )


def get_employee_service(
    session: Session = Depends(get_db),
) -> EmployeeService:
    return EmployeeService(session=session)


def get_credit_service(
    session: Session = Depends(get_db),
) -> CreditService:
    return CreditService(session=session)
