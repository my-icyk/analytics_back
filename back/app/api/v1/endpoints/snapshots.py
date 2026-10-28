from fastapi import APIRouter, Body, Depends, status

from app.api.deps import (
    get_snapshot_service,
    require_permission,
)
from app.core.permisions import PermissionEnum
from app.domains.snapshot import (
    Snapshot,
    SnapshotHistory,
    SnapshotPostResult,
    SnapshotResults,
    SnapshotSave,
)
from app.domains.user import User
from app.services.snapshot import SnapshotService

router = APIRouter(prefix="/snapshots")


@router.get("", response_model=list[Snapshot])
def get_snapshots(
    service: SnapshotService = Depends(get_snapshot_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_SNAPSHOT_READ)),
):
    return service.get_snapshots()


@router.get("/{snapshot_id}", response_model=Snapshot)
def get_snapshot(
    snapshot_id: int,
    service: SnapshotService = Depends(get_snapshot_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_SNAPSHOT_READ)),
):
    return service.get_snapshot(snapshot_id)


@router.get("/{snapshot_id}/results", response_model=list[SnapshotResults])
def get_snapshot_results(
    snapshot_id: int,
    service: SnapshotService = Depends(get_snapshot_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_SNAPSHOT_READ)),
):
    return service.get_results(snapshot_id)


@router.get("/{snapshot_id}/history", response_model=list[SnapshotHistory])
def get_snapshot_history(
    snapshot_id: int,
    service: SnapshotService = Depends(get_snapshot_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_SNAPSHOT_READ)),
):
    return service.get_history(snapshot_id)


@router.post("")
def save_snapshot(
    payload: SnapshotSave,
    service: SnapshotService = Depends(get_snapshot_service),
    user: User = Depends(require_permission(PermissionEnum.FINANCE_SNAPSHOT_SAVE)),
):
    return service.save_snapshot(payload.end_of_month, user)


@router.post("/{snapshot_id}/lock", status_code=status.HTTP_204_NO_CONTENT)
def lock_snapshot(
    snapshot_id: int,
    service: SnapshotService = Depends(get_snapshot_service),
    user: User = Depends(require_permission(PermissionEnum.FINANCE_SNAPSHOT_LOCK)),
    note: str = Body("", embed=True),
):
    service.lock_snapshot(snapshot_id, user, note)


@router.post("/{snapshot_id}/unlock", status_code=status.HTTP_204_NO_CONTENT)
def unlock_snapshot(
    snapshot_id: int,
    service: SnapshotService = Depends(get_snapshot_service),
    user: User = Depends(require_permission(PermissionEnum.FINANCE_SNAPSHOT_UNLOCK)),
    note: str = Body("", embed=True),
):
    service.unlock_snapshot(snapshot_id, user, note)


@router.post("/{snapshot_id}/update", status_code=status.HTTP_204_NO_CONTENT)
def update_snapshot(
    snapshot_id: int,
    service: SnapshotService = Depends(get_snapshot_service),
    user: User = Depends(require_permission(PermissionEnum.FINANCE_SNAPSHOT_UPDATE)),
    note: str = Body("", embed=True),
):
    service.update_snapshot(snapshot_id, user, note)


@router.patch(
    "/{snapshot_id}/results/{resault_id}", status_code=status.HTTP_204_NO_CONTENT
)
def post_result(
    snapshot_id: int,
    resault_id: int,
    payload: SnapshotPostResult,
    service: SnapshotService = Depends(get_snapshot_service),
    _=Depends(require_permission(PermissionEnum.FINANCE_SNAPSHOT_POST)),
):
    service.post_result(snapshot_id, resault_id, payload.is_posted)
