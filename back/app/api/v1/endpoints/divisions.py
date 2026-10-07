from fastapi import APIRouter, Depends, status

from app.api.deps import get_finance_group_service, require_permission
from app.api.v1.schemas.finance import (
    DivisionCreate,
    DivisionDetails,
    DivisionRead,
    DivisionUpdate,
)
from app.core.permisions import PermissionEnum
from app.services.finance_group_service import FinanceGroupService

router = APIRouter(prefix="/divisions")


@router.get("", response_model=list[DivisionDetails])
def get_divisions(
    service: FinanceGroupService = Depends(get_finance_group_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_DIVISION_READ)),
):
    return service.get_divisions()


@router.post("", response_model=DivisionRead)
def create_division(
    payload: DivisionCreate,
    service: FinanceGroupService = Depends(get_finance_group_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_DIVISION_CREATE)),
):
    return service.create_division(payload.name)


@router.put("/{division_id}", response_model=DivisionDetails)
def update_division(
    division_id: int,
    payload: DivisionUpdate,
    service: FinanceGroupService = Depends(get_finance_group_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_DIVISION_UPDATE)),
):
    return service.update_division(division_id, payload.name)


@router.delete("/{division_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_division(
    division_id: int,
    service: FinanceGroupService = Depends(get_finance_group_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_DIVISION_DELETE)),
):
    service.delete_division(division_id)
