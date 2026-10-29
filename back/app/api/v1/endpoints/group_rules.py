from fastapi import APIRouter, Depends, status

from app.api.deps import (
    get_finance_rule_service,
    require_permission,
)
from app.api.v1.schemas.finance import (
    CopyTargetsIn,
    RuleCreate,
    RuleRead,
    RuleUpdate,
    TargetCreate,
    TargetRead,
    TargetUpdate,
)
from app.core.permisions import PermissionEnum
from app.services.finance_rule_service import FinanceRuleService

router = APIRouter(prefix="/groups/{group_id}/rules")


@router.get("/{id}", response_model=RuleRead)
def get_rule(
    group_id: int,
    id: int,
    service: FinanceRuleService = Depends(get_finance_rule_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_RULE_READ)),
):
    return service.get_rule(id)


@router.post("")
def create_rule(
    group_id: int,
    payload: RuleCreate,
    service: FinanceRuleService = Depends(get_finance_rule_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_RULE_CREATE)),
):
    # TODO: CREATE COMMANDS
    id = service.create_rule(
        group_id,
        payload.name,
        payload.valid_from,
        payload.valid_to,
        payload.percent_value,
    )
    return {"id": id}


@router.put("/{rule_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_rule(
    group_id: int,
    rule_id: int,
    payload: RuleUpdate,
    service: FinanceRuleService = Depends(get_finance_rule_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_RULE_UPDATE)),
):
    service.update_rule(
        group_id,
        rule_id,
        payload.name,
        payload.valid_from,
        payload.valid_to,
        payload.percent_value,
    )


@router.delete("/{rule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rule(
    group_id: int,
    rule_id: int,
    service: FinanceRuleService = Depends(get_finance_rule_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_RULE_DELETE)),
):
    service.delete_rule(group_id, rule_id)


@router.get("/{rule_id}/targets", response_model=list[TargetRead])
def get_targets(
    rule_id: int,
    service: FinanceRuleService = Depends(get_finance_rule_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_RULE_TARGET_READ)),
):
    return service.get_targets(rule_id)


@router.post("/{rule_id}/targets")
def assign_target(
    rule_id: int,
    payload: TargetCreate,
    service: FinanceRuleService = Depends(get_finance_rule_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_RULE_TARGET_CREATE)),
):
    id = service.assign_target(
        rule_id=rule_id,
        group_id=payload.group_id,
        allocation_type=payload.allocation_type,
        percent_value=payload.percent_value,
    )
    return {"id": id}


@router.put("/{rule_id}/targets/{target_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_target(
    rule_id: int,
    target_id: int,
    payload: TargetUpdate,
    service: FinanceRuleService = Depends(get_finance_rule_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_RULE_TARGET_UPDATE)),
):
    service.update_target(
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
    _=Depends(require_permission(PermissionEnum.FINANCE_RULE_TARGET_DELETE)),
):
    service.remove_target(rule_id, target_id)


@router.post("/{rule_id}/targets/copy-from", status_code=status.HTTP_204_NO_CONTENT)
def replace_targets_from_rule(
    rule_id: int,
    payload: CopyTargetsIn,
    service: FinanceRuleService = Depends(get_finance_rule_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_RULE_TARGET_UPDATE)),
):
    service.replace_targets_from_rule(rule_id, payload.source_rule_id)
