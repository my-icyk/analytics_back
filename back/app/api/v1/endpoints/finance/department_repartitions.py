from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.deps import get_finance_group_service, require_permission
from app.api.v1.schemas.common import Page
from app.core.permisions import PermissionEnum
from app.domains.user import User
from app.filters.finance import DepartmentRepartitionFilter
from app.read_models.finance import DepartmentRepartitionDetails
from app.services.finance_group_service import FinanceGroupService

router = APIRouter()


@router.get("", response_model=Page[DepartmentRepartitionDetails])
def list_department_repartitions(
    params: Annotated[DepartmentRepartitionFilter, Query()],
    caller: User = Depends(
        require_permission(PermissionEnum.FINANCE_DEPARTMENT_REPARTITION_READ)
    ),
    service: FinanceGroupService = Depends(get_finance_group_service),
):
    items, total = service.list_department_repartitions(caller, params)
    return Page(
        items=items,
        total=total,
        page=params.page,
        limit=params.limit,
    )
