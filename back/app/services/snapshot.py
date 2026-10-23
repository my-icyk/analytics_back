from datetime import date

from app.domains.snapshot import Snapshot
from app.exceptions.exceptions import AlreadyExistsError, ForbiddenError, NotFoundError
from app.repositories.snapshot_repository import SnapshotRepository


class SnapshotService:
    def __init__(
        self,
        snapshot_repository: SnapshotRepository,
    ):
        self.snapshot_repository = snapshot_repository

    def _validate_locked(self, snapshot_id: int) -> None:
        snapshot = self.get_snapshot(snapshot_id)
        if snapshot.is_locked:
            raise ForbiddenError(f"Month {snapshot.end_of_month} is locked")

    def get_snapshots(self) -> list[Snapshot]:
        return self.snapshot_repository.get_snapshots()

    def get_snapshot(self, snapshot_id: int) -> Snapshot:
        snapshot = self.snapshot_repository.get_snapshot(snapshot_id)
        if not snapshot:
            raise NotFoundError("Snapshot", "id", str(snapshot_id))
        return snapshot

    def get_results(self, snapshot_id: int):
        return self.snapshot_repository.get_results(snapshot_id)

    def get_history(self, snapshot_id: int):
        return self.snapshot_repository.get_history(snapshot_id)

    def save_snapshot(self, end_of_month: date, user_id: int) -> int:
        if self.snapshot_repository.exist_by_month(end_of_month):
            raise AlreadyExistsError("Snapshot", "end_of_month", str(end_of_month))
        return self.snapshot_repository.save(end_of_month, user_id)

    def lock_snapshot(self, snapshot_id: int, user_id: int, note: str) -> None:
        self._validate_locked(snapshot_id)

        self.snapshot_repository.lock(snapshot_id, user_id, note)

    def unlock_snapshot(self, snapshot_id: int, user_id: int, note: str) -> None:
        self.get_snapshot(snapshot_id)

        self.snapshot_repository.unlock(snapshot_id, user_id, note)

    def update_snapshot(self, snapshot_id: int, user_id: int, note: str) -> None:
        self._validate_locked(snapshot_id)

        self.snapshot_repository.update(snapshot_id, user_id, note)

    def post_result(self, snapshot_id: int, resault_id: int, is_posted: bool) -> None:
        self._validate_locked(snapshot_id)

        self.snapshot_repository.post(snapshot_id, resault_id, is_posted)
