from fastapi import APIRouter, Depends

from app.api.deps import get_specific_service, require_permission
from app.core.permisions import PermissionEnum
from app.domains.specific_models import ProductSummary
from app.services.specific_service import SpecificService

router = APIRouter(prefix="/specific", tags=["specific"])


@router.get("/product-summary/{product_code}", response_model=ProductSummary)
def GetProductSummaryByCode(
    product_code: str,
    service: SpecificService = Depends(get_specific_service),
    _=Depends(require_permission(PermissionEnum.PRODUCT_PRICES_READ)),
):
    return service.exec_price_for_nomen_for_api(product_code)
