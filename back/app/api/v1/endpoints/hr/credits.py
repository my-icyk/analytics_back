from fastapi import APIRouter, Depends, Query

from app.api.deps import get_credit_service, require_permission
from app.api.schemas.employee import (
    CreditCreate,
    CreditDetail,
    CreditRead,
    CreditStatus,
    Page,
    PositiveId,
)
from app.core.permisions import PermissionEnum
from app.services.employees.credit_service import CreditService

router = APIRouter()


@router.get(
    "",
    response_model=Page[CreditRead],
    dependencies=[Depends(require_permission(PermissionEnum.HR_CREDIT_READ))],
)
def list_credits(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0, le=2147483647),
    employee_ids: list[PositiveId] | None = Query(None, max_length=200),
    statuses: list[CreditStatus] | None = Query(None, max_length=3),
    search: str | None = Query(None, max_length=255),
    service: CreditService = Depends(get_credit_service),
):
    items, total = service.get_page(
        limit=limit,
        offset=offset,
        employee_ids=employee_ids,
        statuses=statuses,
        search=search,
    )
    return Page[CreditRead](
        items=[CreditRead.model_validate(item, from_attributes=True) for item in items],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.post(
    "",
    response_model=CreditDetail,
    status_code=201,
)
def create_credit(
    data: CreditCreate,
    current_user=Depends(require_permission(PermissionEnum.HR_CREDIT_CREATE)),
    service: CreditService = Depends(get_credit_service),
):

    return service.create(data, created_by=current_user.id)
