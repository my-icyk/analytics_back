from fastapi import APIRouter, Depends

from app.api.deps import get_finance_group_service, require_permission
from app.api.v1.schemas.finance import CompanyRead
from app.core.permisions import PermissionEnum
from app.domains.user import User
from app.services.finance_group_service import FinanceGroupService

router = APIRouter()


@router.get("", response_model=list[CompanyRead])
def list_companies(
    _: User = Depends(require_permission(PermissionEnum.FINANCE_COMPANY_READ)),
    service: FinanceGroupService = Depends(get_finance_group_service),
):

    return service.get_companies()
