from datetime import date, datetime

from app.domains.domain_model import DomainModel


class Snapshot(DomainModel):
    id: int
    end_of_month: date
    is_locked: bool
    groups_count: int
    posted_count: int
    created_at: datetime
    updated_at: datetime


class SnapshotSave(DomainModel):
    end_of_month: date


class SnapshotPostResult(DomainModel):
    is_posted: bool


class SnapshotHistory(DomainModel):
    id: int
    snapshot_id: int
    user_id: int
    user_name: str
    action_type: str
    notes: str | None
    created_at: datetime


class SnapshotResults(DomainModel):
    id: int
    snapshot_id: int
    group_id: int
    group_name: str
    division_name: str
    is_posted: bool
