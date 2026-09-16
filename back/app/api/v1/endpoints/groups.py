from fastapi import APIRouter, Depends, status

from app.api.deps import (
    get_finance_group_service,
    get_finance_rule_service,
    require_permission,
)
from app.api.v1.schemas.finance import (
    GroupCreate,
    GroupRead,
    GroupTypeRead,
    GroupUpdate,
    RuleRead,
)
from app.core.permisions import PermissionEnum
from app.services.finance_group_service import FinanceGroupService
from app.services.finance_rule_service import FinanceRuleService

router = APIRouter(prefix="/groups")


@router.get("/types", response_model=list[GroupTypeRead])
def get_group_types(
    service: FinanceGroupService = Depends(get_finance_group_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_GROUP_READ)),
):
    return service.get_group_types()


@router.get("", response_model=list[GroupRead])
def get_groups(
    service: FinanceGroupService = Depends(get_finance_group_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_GROUP_READ)),
):
    return service.get_groups()


@router.get("/{id}", response_model=GroupRead)
def get_group(
    id: int,
    service: FinanceGroupService = Depends(get_finance_group_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_GROUP_READ)),
):
    return service.get_group(id)


@router.post("", response_model=GroupRead)
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
