from fastapi import APIRouter, Depends, Query, status

from app.api.deps import (
    get_finance_group_service,
    get_finance_rule_service,
    require_permission,
)
from app.api.v1.schemas.common import PaginatedResponse
from app.api.v1.schemas.finance import (
    DepartmentRead,
    DepartmentRepartitionCreate,
    DepartmentRepartitionRead,
    GroupCreate,
    GroupRead,
    GroupTypeRead,
    GroupUpdate,
    RuleRead,
)
from app.core.permisions import PermissionEnum
from app.domains.finance import GroupFilter
from app.services.finance_group_service import FinanceGroupService
from app.services.finance_rule_service import FinanceRuleService

router = APIRouter(prefix="/groups")


@router.get("/departments", response_model=list[DepartmentRead])
def get_departments(
    service: FinanceGroupService = Depends(get_finance_group_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_DEPARTMENT_REPARTITION_READ)),
):
    return service.get_departments()


@router.get("/types", response_model=list[GroupTypeRead])
def get_group_types(
    service: FinanceGroupService = Depends(get_finance_group_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_GROUP_READ)),
):
    return service.get_group_types()


@router.get("", response_model=PaginatedResponse[GroupRead])
def get_groups(
    search: str | None = Query(None),
    division_ids: list[int] | None = Query(None),
    group_type_ids: list[int] | None = Query(None),
    limit: int = Query(50, le=200, ge=1),
    offset: int = Query(0, ge=0),
    service: FinanceGroupService = Depends(get_finance_group_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_GROUP_READ)),
):

    filters = GroupFilter(
        search=search,
        division_ids=division_ids,
        group_type_ids=group_type_ids,
        limit=limit,
        offset=offset,
    )

    page = service.get_groups_page(filters)

    return PaginatedResponse(
        items=page.items,
        total=page.total,
        limit=limit,
        offset=offset,
    )


@router.get("/{id}", response_model=GroupRead)
def get_group(
    id: int,
    service: FinanceGroupService = Depends(get_finance_group_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_GROUP_READ)),
):
    return service.get_group(id)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=GroupRead,
)
def create_group(
    payload: GroupCreate,
    service: FinanceGroupService = Depends(get_finance_group_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_GROUP_CREATE)),
):
    return service.create_group(
        payload.name, payload.group_type_id, payload.division_id
    )


@router.put("/{id}", response_model=GroupRead)
def update_group(
    id: int,
    payload: GroupUpdate,
    service: FinanceGroupService = Depends(get_finance_group_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_GROUP_UPDATE)),
):
    return service.update_group(
        id, payload.name, payload.group_type_id, payload.division_id
    )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group(
    id: int,
    service: FinanceGroupService = Depends(get_finance_group_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_GROUP_DELETE)),
):
    return service.delete_group(id)


@router.get("/{id}/rules", response_model=list[RuleRead])
def get_rules(
    id: int,
    service: FinanceRuleService = Depends(get_finance_rule_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_RULE_READ)),
):
    return service.get_rules_by_group_id(id)


@router.get("/{id}/departments", response_model=list[DepartmentRepartitionRead])
def get_department_repartitions(
    id: int,
    service: FinanceGroupService = Depends(get_finance_group_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_DEPARTMENT_REPARTITION_READ)),
):
    return service.get_department_repartition(id)


@router.post(
    "/{id}/departments",
    status_code=status.HTTP_201_CREATED,
    response_model=DepartmentRepartitionRead,
)
def create_department_repartition(
    id: int,
    payload: DepartmentRepartitionCreate,
    service: FinanceGroupService = Depends(get_finance_group_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_DEPARTMENT_REPARTITION_CREATE)),
):
    return service.create_department_repartition(
        payload.department_id, id, payload.valid_from, payload.valid_to
    )
