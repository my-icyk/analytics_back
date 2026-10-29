from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.api.deps import (
    get_finance_group_service,
    get_finance_rule_service,
    require_permission,
)
from app.api.v1.schemas.common import Page
from app.api.v1.schemas.finance import (
    DepartmentRead,
    DepartmentRepartitionCreate,
    DepartmentRepartitionRead,
    DepartmentRepartitionUpdate,
    GroupCreate,
    GroupOverview,
    GroupRead,
    GroupTypeDetails,
    GroupUpdate,
    RuleRead,
)
from app.core.permisions import PermissionEnum
from app.filters.finance import GroupFilter
from app.repositories.base import LookupResponse
from app.services.finance_group_service import FinanceGroupService
from app.services.finance_rule_service import FinanceRuleService

router = APIRouter(prefix="/groups")


@router.get("/departments", response_model=list[DepartmentRead])
def get_departments(
    service: FinanceGroupService = Depends(get_finance_group_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_DEPARTMENT_REPARTITION_READ)),
):
    return service.get_departments()


@router.get("/departments/lookup", response_model=list[LookupResponse])
def lookup_departments(
    search: str = Query(...),
    service: FinanceGroupService = Depends(get_finance_group_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_DEPARTMENT_REPARTITION_READ)),
):
    return service.lookup_departments(search)


@router.get("/types", response_model=list[GroupTypeDetails])
def get_group_types(
    service: FinanceGroupService = Depends(get_finance_group_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_GROUP_READ)),
):
    return service.get_group_types()


@router.get("/lookup", response_model=list[LookupResponse])
def lookup_groups(
    search: str = Query(None),
    service: FinanceGroupService = Depends(get_finance_group_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_GROUP_READ)),
):
    return service.lookup_groups(search)


@router.get("", response_model=Page[GroupRead])
def get_groups(
    params: Annotated[GroupFilter, Query()],
    service: FinanceGroupService = Depends(get_finance_group_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_GROUP_READ)),
):

    rows = service.get_groups_page(params)

    return Page(
        items=rows.items,
        total=rows.total,
        page=params.page,
        limit=params.limit,
    )


@router.get("/{id}", response_model=GroupOverview)
def get_group(
    id: int,
    service: FinanceGroupService = Depends(get_finance_group_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_GROUP_READ)),
):
    return service.get_group(id)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
def create_group(
    payload: GroupCreate,
    service: FinanceGroupService = Depends(get_finance_group_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_GROUP_CREATE)),
):
    id = service.create_group(payload.name, payload.group_type_id, payload.division_id)
    return {"id": id}


@router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_group(
    id: int,
    payload: GroupUpdate,
    service: FinanceGroupService = Depends(get_finance_group_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_GROUP_UPDATE)),
):
    service.update_group(id, payload.name, payload.group_type_id, payload.division_id)


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


@router.get("/{id}/repartitions", response_model=list[DepartmentRepartitionRead])
def get_department_repartitions(
    id: int,
    service: FinanceGroupService = Depends(get_finance_group_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_DEPARTMENT_REPARTITION_READ)),
):
    return service.get_department_repartition(id)


@router.post(
    "/{id}/repartitions",
    status_code=status.HTTP_201_CREATED,
)
def create_department_repartition(
    id: int,
    payload: DepartmentRepartitionCreate,
    service: FinanceGroupService = Depends(get_finance_group_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_DEPARTMENT_REPARTITION_CREATE)),
):
    id = service.create_department_repartition(
        payload.department_id, id, payload.valid_from, payload.valid_to
    )
    return {"id": id}


@router.put(
    "/{group_id}/repartitions/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def update_department_repartition(
    group_id: int,
    id: int,
    payload: DepartmentRepartitionUpdate,
    service: FinanceGroupService = Depends(get_finance_group_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_DEPARTMENT_REPARTITION_UPDATE)),
):
    # TODO: de exclus return statment
    service.update_department_repartition(
        id, payload.department_id, group_id, payload.valid_from, payload.valid_to
    )


@router.delete(
    "/{group_id}/repartitions/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_department_repartition(
    group_id: int,
    id: int,
    service: FinanceGroupService = Depends(get_finance_group_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_DEPARTMENT_REPARTITION_DELETE)),
):
    service.delete_department_repartition(id, group_id)
