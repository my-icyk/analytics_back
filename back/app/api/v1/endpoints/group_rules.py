from fastapi import APIRouter, Depends, status

from app.api.deps import (
    get_finance_rule_service,
    require_permission,
)
from app.api.v1.schemas.finance import (
    RuleCreate,
    RuleRead,
    RuleUpdate,
    TargetCreate,
    TargetRead,
    TargetUpdate,
)
from app.core.permisions import PermissionEnum
from app.services.finance_rule_service import FinanceRuleService

router = APIRouter(prefix="/rules")


@router.get("/{id}", response_model=RuleRead)
def get_rule(
    id: int,
    service: FinanceRuleService = Depends(get_finance_rule_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_RULE_READ)),
):
    return service.get_rule(id)


@router.post("", response_model=RuleRead)
def create_rule(
    payload: RuleCreate,
    service: FinanceRuleService = Depends(get_finance_rule_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_RULE_CREATE)),
):
    # TODO: CREATE COMMANDS
    return service.create_rule(
        payload.name,
        payload.group_id,
        payload.valid_from,
        payload.valid_to,
        payload.percent_value,
    )


@router.put("/{rule_id}", response_model=RuleRead)
def update_rule(
    rule_id: int,
    payload: RuleUpdate,
    service: FinanceRuleService = Depends(get_finance_rule_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_RULE_UPDATE)),
):
    return service.update_rule(
        rule_id,
        payload.name,
        payload.group_id,
        payload.valid_from,
        payload.valid_to,
        payload.percent_value,
    )


@router.delete("/{rule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rule(
    rule_id: int,
    service: FinanceRuleService = Depends(get_finance_rule_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_RULE_DELETE)),
):
    service.delete_rule(rule_id)


@router.get("/{rule_id}/targets", response_model=list[TargetRead])
def get_targets(
    rule_id: int,
    service: FinanceRuleService = Depends(get_finance_rule_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_RULE_READ)),
):
    return service.get_targets(rule_id)


@router.post("/{rule_id}/targets", response_model=TargetRead)
def assign_target(
    rule_id: int,
    payload: TargetCreate,
    service: FinanceRuleService = Depends(get_finance_rule_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_RULE_CREATE)),
):
    return service.assign_target(
        rule_id=rule_id,
        group_id=payload.group_id,
        allocation_type=payload.allocation_type,
        percent_value=payload.percent_value,
    )


@router.put("/{rule_id}/targets/{target_id}", response_model=TargetRead)
def update_target(
    rule_id: int,
    target_id: int,
    payload: TargetUpdate,
    service: FinanceRuleService = Depends(get_finance_rule_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_RULE_UPDATE)),
):
    return service.update_target(
        id=target_id,
        rule_id=rule_id,
        group_id=payload.group_id,
        allocation_type=payload.allocation_type,
        percent_value=payload.percent_value,
    )


@router.delete("/{rule_id}/targets/{target_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_target(
    rule_id: int,
    target_id: int,
    service: FinanceRuleService = Depends(get_finance_rule_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_RULE_DELETE)),
):
    service.remove_target(target_id, rule_id)
