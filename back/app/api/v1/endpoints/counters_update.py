from fastapi import APIRouter, Depends

from app.api.deps import get_counter_update_service, get_current_user
from app.models.user import User
from app.schemas.counter_update_schema import (
    CounterUpdateListQuery,
    CounterUpdateListResponse,
    CounterUpdateViewSchema,
)
from app.services.counter_update_service import CounterUpdateService

router = APIRouter(prefix="/counters_update", tags=["counters_update"])


@router.get("/", response_model=CounterUpdateListResponse)
def get_all(
    query: CounterUpdateListQuery = Depends(),
    service: CounterUpdateService = Depends(get_counter_update_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_all(current_user, query)


@router.get("/{counter_update_id}", response_model=CounterUpdateViewSchema)
def get_by_id(
    counter_update_id: int,
    service: CounterUpdateService = Depends(get_counter_update_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_by_id(
        current_user=current_user, counter_update_id=counter_update_id
    )
