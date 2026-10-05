from fastapi import APIRouter, Depends, status

from app.api.deps import get_counter_update_service, require_permission
from app.core.permisions import PermissionEnum
from app.schemas.counter_update_schema import (
    CounterExceptionsCreate,
    CounterExceptionsUpdate,
    CounterExceptionsView,
    CountersRead,
)
from app.services.counter_update_service import CounterUpdateService

counter_router = APIRouter(prefix="/counters", tags=["counters"])


@counter_router.get("", response_model=list[CountersRead])
def get_counters(
    service: CounterUpdateService = Depends(get_counter_update_service),
    _=Depends(require_permission(PermissionEnum.COUNTER_UPDATE_READ)),
):
    return service.get_counters()


@counter_router.get(
    "/{counter_id}/exceptions", response_model=list[CounterExceptionsView]
)
def get_by_counter_id(
    counter_id: int,
    service: CounterUpdateService = Depends(get_counter_update_service),
    _=Depends(require_permission(PermissionEnum.COUNTER_UPDATE_READ)),
):
    return service.get_by_counter_id(counter_id)


exceptions_router = APIRouter(prefix="/counter-exceptions", tags=["counters"])


@exceptions_router.get("/{exception_id}", response_model=CounterExceptionsView)
def get_by_id(
    exception_id: int,
    service: CounterUpdateService = Depends(get_counter_update_service),
    _=Depends(require_permission(PermissionEnum.COUNTER_UPDATE_READ)),
):
    return service.get_by_id(exception_id=exception_id)


@exceptions_router.post("", status_code=status.HTTP_201_CREATED)
def create(
    data: CounterExceptionsCreate,
    service: CounterUpdateService = Depends(get_counter_update_service),
    user_id=Depends(require_permission(PermissionEnum.COUNTER_UPDATE_CREATE)),
):

    service.create(data, user_id=user_id)


@exceptions_router.put("/{exception_id}", status_code=status.HTTP_204_NO_CONTENT)
def update(
    exception_id: int,
    data: CounterExceptionsUpdate,
    service: CounterUpdateService = Depends(get_counter_update_service),
    _=Depends(require_permission(PermissionEnum.COUNTER_UPDATE_UPDATE)),
):

    service.update(exception_id, data)


@exceptions_router.delete("/{exception_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    exception_id: int,
    service: CounterUpdateService = Depends(get_counter_update_service),
    _=Depends(require_permission(PermissionEnum.COUNTER_UPDATE_DELETE)),
):
    service.delete(exception_id)
