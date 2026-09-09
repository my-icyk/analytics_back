from fastapi import APIRouter, Depends

from app.api.deps import get_current_user, get_specific_service
from app.models.specific_models import ProductSummary
from app.models.user import User
from app.services.specific_service import SpecificService

router = APIRouter(prefix="/specific", tags=["specific"])


@router.get("/product-summary/{product_code}", response_model=ProductSummary)
def GetProductSummaryByCode(
    product_code: str,
    service: SpecificService = Depends(get_specific_service),
    current_user: User = Depends(get_current_user),
):
    return service.exec_price_for_nomen_for_api(product_code, current_user)
