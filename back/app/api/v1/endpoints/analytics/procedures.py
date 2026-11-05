from fastapi import APIRouter, Depends, status

from app.api.deps import get_procedure_service, require_permission
from app.api.v1.schemas.analytics import ProcedureCreate, ProcedureUpdate
from app.api.v1.schemas.common import IdResponse
from app.core.permisions import PermissionEnum
from app.domains.analytics.procedure import Procedure, ProcedureHistory
from app.domains.user import User
from app.services.analytics.procedure_service import ProcedureService

router = APIRouter()


@router.get("", response_model=list[Procedure])
def list_procedures(
    _: User = Depends(require_permission(PermissionEnum.ANALYTICS_PROCEDURE_READ)),
    service: ProcedureService = Depends(get_procedure_service),
):
    return service.get_all()


@router.get("/{id}", response_model=Procedure)
def get_procedure(
    id: int,
    _: User = Depends(require_permission(PermissionEnum.ANALYTICS_PROCEDURE_READ)),
    service: ProcedureService = Depends(get_procedure_service),
):
    return service.get_by_id(id)


@router.post("", response_model=IdResponse)
def create_procedure(
    payload: ProcedureCreate,
    _: User = Depends(require_permission(PermissionEnum.ANALYTICS_PROCEDURE_CREATE)),
    service: ProcedureService = Depends(get_procedure_service),
):
    id = service.create(payload.name, payload.exec_order)
    return IdResponse(id=id)


@router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_procedure(
    id: int,
    payload: ProcedureUpdate,
    _: User = Depends(require_permission(PermissionEnum.ANALYTICS_PROCEDURE_UPDATE)),
    service: ProcedureService = Depends(get_procedure_service),
):
    service.update(id, payload.name, payload.exec_order, payload.is_active)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_procedure(
    id: int,
    _: User = Depends(require_permission(PermissionEnum.ANALYTICS_PROCEDURE_DELETE)),
    service: ProcedureService = Depends(get_procedure_service),
):
    service.delete(id)


@router.get("/{id}/history", response_model=list[ProcedureHistory])
def get_procedure_history(
    id: int,
    _: User = Depends(require_permission(PermissionEnum.ANALYTICS_PROCEDURE_READ)),
    service: ProcedureService = Depends(get_procedure_service),
):
    return service.get_last_history_by_id(id)


@router.post("/{id}/run", status_code=status.HTTP_204_NO_CONTENT)
def run_procedure(
    id: int,
    _: User = Depends(require_permission(PermissionEnum.ANALYTICS_PROCEDURE_RUN)),
    service: ProcedureService = Depends(get_procedure_service),
):
    service.run_by_id(id)
