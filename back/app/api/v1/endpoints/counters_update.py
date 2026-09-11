from fastapi import APIRouter, Depends, status

from app.api.deps import get_counter_update_service, require_permission
from app.core.permisions import PermissionEnum
from app.schemas.counter_update_schema import (
    CountersUpdateCreate,
    CounterUpdateListQuery,
    CounterUpdateListResponse,
    CounterUpdateView,
)
from app.services.counter_update_service import CounterUpdateService

router = APIRouter(prefix="/counter-updates", tags=["counter-updates"])


@router.get("", response_model=CounterUpdateListResponse)
def get_all(
    query: CounterUpdateListQuery = Depends(),
    service: CounterUpdateService = Depends(get_counter_update_service),
    _=Depends(require_permission(PermissionEnum.COUNTER_UPDATE_READ)),
):
    return service.get_all(query)


@router.get("/{counter_update_id}", response_model=CounterUpdateView)
def get_by_id(
    counter_update_id: int,
    service: CounterUpdateService = Depends(get_counter_update_service),
    _=Depends(require_permission(PermissionEnum.COUNTER_UPDATE_READ)),
):
    return service.get_by_id(counter_update_id=counter_update_id)


@router.post("", status_code=status.HTTP_201_CREATED)
def create(
    data: CountersUpdateCreate,
    service: CounterUpdateService = Depends(get_counter_update_service),
    _=Depends(require_permission(PermissionEnum.COUNTER_UPDATE_CREATE)),
):

    service.create(data)


@router.put("/{counter_update_id}", status_code=status.HTTP_204_NO_CONTENT)
def update(
    counter_update_id: int,
    data: CountersUpdateCreate,
    service: CounterUpdateService = Depends(get_counter_update_service),
    _=Depends(require_permission(PermissionEnum.COUNTER_UPDATE_UPDATE)),
):

    service.update(counter_update_id, data)


@router.delete("/{counter_update_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    counter_update_id: int,
    service: CounterUpdateService = Depends(get_counter_update_service),
    _=Depends(require_permission(PermissionEnum.COUNTER_UPDATE_DELETE)),
):
    service.delete(counter_update_id)
