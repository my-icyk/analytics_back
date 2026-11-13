from fastapi import Depends
from fastapi.security import APIKeyCookie
from sqlalchemy.orm import Session

from app.config import get_settings
from app.core.permisions import PermissionEnum
from app.db.database import get_db
from app.db.models.auth import User
from app.repositories.analytics.procedure_repository import ProcedureRepository
from app.repositories.auth import UserRepository
from app.repositories.auth.authorization_repository import AuthorizationRepository
from app.repositories.auth.permision_repository import PermissionRepository
from app.repositories.auth.role_permission_repository import RolePermissionRepository
from app.repositories.auth.role_repository import RoleRepository
from app.repositories.auth.session_repository import SessionRepository
from app.repositories.auth.user_role_repository import UserRoleRepository
from app.repositories.counter_update_repository import CounterUpdateRepository
from app.repositories.department_repartition import DepartmentRepartitionRepository
from app.repositories.division_repository import DivisionRepository
from app.repositories.finance.company_repo import CompanyRepo
from app.repositories.group_repository import GroupRepository
from app.repositories.group_rule_repository import GroupRuleRepository
from app.repositories.group_rule_target_repository import GroupRuleTargetRepository
from app.repositories.group_type_repository import GroupTypeRepository
from app.repositories.snapshot_repository import SnapshotRepository
from app.repositories.specific_repository import SpecificRepository
from app.services.analytics.procedure_service import ProcedureService
from app.services.auth.authentication_service import AuthenticationService
from app.services.auth.authorization_service import AuthorizationService
from app.services.auth.user_service import UserService
from app.services.counter_update_service import CounterUpdateService
from app.services.employees.credit_service import CreditService
from app.services.employees.employee_service import EmployeeService
from app.services.finance_group_service import FinanceGroupService
from app.services.finance_rule_service import FinanceRuleService
from app.services.role_permission_service import RolePermissionService
from app.services.snapshot import SnapshotService
from app.services.specific_service import SpecificService

settings = get_settings()
session_cookie = APIKeyCookie(name=settings.SESSION_COOKIE_NAME, auto_error=False)


# TODO: WTF HERE IS HAPPENDS
def get_specific_repository(db: Session = Depends(get_db)) -> SpecificRepository:
    return SpecificRepository(db)


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_role_repository(db: Session = Depends(get_db)) -> RoleRepository:
    return RoleRepository(db)


def get_department_repartition_repository(
    db: Session = Depends(get_db),
) -> DepartmentRepartitionRepository:
    return DepartmentRepartitionRepository(db)


def get_user_role_repository(db: Session = Depends(get_db)) -> UserRoleRepository:
    return UserRoleRepository(db)


def get_permission_repository(db: Session = Depends(get_db)) -> PermissionRepository:
    return PermissionRepository(db)


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
def get_auth_service(db: Session = Depends(get_db)) -> AuthenticationService:
    return AuthenticationService(db, SessionRepository(db))


def get_specific_service(
    specific_repo: SpecificRepository = Depends(get_specific_repository),
) -> SpecificService:
    return SpecificService(specific_repo)


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(
        session=db,
        user_repository=UserRepository(db),
    )


def get_role_permission_service(
    db: Session = Depends(get_db),
) -> RolePermissionService:
    return RolePermissionService(
        session=db,
        role_repository=RoleRepository(db),
        permission_repository=PermissionRepository(db),
        role_permission_repository=RolePermissionRepository(db),
        user_role_repository=UserRoleRepository(db),
        user_repository=UserRepository(db),
    )


def get_counter_update_service(
    counter_update_repo: CounterUpdateRepository = Depends(
        get_counter_update_repository
    ),
) -> CounterUpdateService:
    return CounterUpdateService(counter_update_repo)


def get_authorization_service(
    db: Session = Depends(get_db),
) -> AuthorizationService:
    return AuthorizationService(
        authorization_repo=AuthorizationRepository(db),
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


def get_company_repository(db: Session = Depends(get_db)) -> CompanyRepo:
    return CompanyRepo(db)


def get_finance_group_service(
    session: Session = Depends(get_db),
) -> FinanceGroupService:
    return FinanceGroupService(
        group_type_repository=GroupTypeRepository(session),
        division_repository=DivisionRepository(session),
        group_repository=GroupRepository(session),
        group_rule_repository=GroupRuleRepository(session),
        department_repartition_repository=DepartmentRepartitionRepository(session),
        company_repo=CompanyRepo(session),
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


def get_snapshot_repository(db: Session = Depends(get_db)) -> SnapshotRepository:
    return SnapshotRepository(db)


def get_snapshot_service(
    snapshot_repository: SnapshotRepository = Depends(get_snapshot_repository),
) -> SnapshotService:
    return SnapshotService(
        snapshot_repository=snapshot_repository,
    )


def get_procedure_repository(db: Session = Depends(get_db)) -> ProcedureRepository:
    return ProcedureRepository(db)


def get_procedure_service(
    procedure_repository: ProcedureRepository = Depends(get_procedure_repository),
) -> ProcedureService:
    return ProcedureService(
        procedure_repository=procedure_repository,
    )


def get_employee_service(
    session: Session = Depends(get_db),
) -> EmployeeService:
    return EmployeeService(session=session)


def get_credit_service(
    session: Session = Depends(get_db),
) -> CreditService:
    return CreditService(session=session)
