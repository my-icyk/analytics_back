from fastapi import APIRouter, Depends, Path, Query, Response, status

from app.api.deps import get_credit_service, require_permission
from app.api.schemas.hr import (
    CreditCreate,
    CreditDetail,
    CreditPayOff,
    CreditRead,
    CreditStatus,
    CreditUpdate,
    Page,
    PositiveId,
)
from app.api.v1.schemas.common import IdResponse
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


@router.get(
    "/{credit_id}",
    response_model=CreditDetail,
    dependencies=[Depends(require_permission(PermissionEnum.HR_CREDIT_READ))],
)
def get_credit(
    credit_id: PositiveId,
    service: CreditService = Depends(get_credit_service),
):
    return service.get(credit_id)


@router.post(
    "",
    response_model=IdResponse,
    status_code=201,
)
def create_credit(
    data: CreditCreate,
    current_user=Depends(require_permission(PermissionEnum.HR_CREDIT_CREATE)),
    service: CreditService = Depends(get_credit_service),
):

    id = service.create(data, created_by=current_user.id)
    return IdResponse(id=id)


@router.put(
    "/{credit_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_permission(PermissionEnum.HR_CREDIT_CREATE))],
)
def update_credit(
    data: CreditUpdate,
    credit_id: int = Path(gt=0, le=2147483647),
    service: CreditService = Depends(get_credit_service),
):
    service.update(credit_id, data)


@router.post(
    "/{credit_id}/pay-off",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_permission(PermissionEnum.HR_CREDIT_CREATE))],
)
def pay_off_credit(
    data: CreditPayOff,
    credit_id: int = Path(gt=0, le=2147483647),
    service: CreditService = Depends(get_credit_service),
):
    service.pay_off(credit_id, data.paid_off_on)


@router.post(
    "/{credit_id}/cancel",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_permission(PermissionEnum.HR_CREDIT_CREATE))],
)
def cancel_credit(
    credit_id: int = Path(gt=0, le=2147483647),
    service: CreditService = Depends(get_credit_service),
):
    service.cancel(credit_id)


@router.delete(
    "/{credit_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_permission(PermissionEnum.HR_CREDIT_DELETE))],
)
def delete_credit(
    credit_id: int = Path(gt=0, le=2147483647),
    service: CreditService = Depends(get_credit_service),
) -> Response:
    service.delete(credit_id)
    return Response(status_code=204)
