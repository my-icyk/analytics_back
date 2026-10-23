from datetime import date

from app.domains.snapshot import Snapshot, SnapshotHistory, SnapshotResults
from app.repositories.base import BaseRepository


class SnapshotRepository(BaseRepository):
    def exist_by_month(self, end_of_month: date) -> bool:
        sql = """
       SELECT CASE WHEN EXISTS (
           SELECT 1 FROM finance.snapshot WHERE end_of_month = :end_of_month
       ) THEN 1 ELSE 0 END AS found
       """
        row = self._scalar(sql, {"end_of_month": end_of_month})
        return bool(row)

    def get_snapshots(self) -> list[Snapshot]:
        sql = """
        SELECT
            id, 
            end_of_month,
            groups_count = (SELECT count(*) FROM finance.snapshot_financial_results as notmain WHERE notmain.snapshot_id = main.id),
            posted_count = (SELECT count(*) FROM finance.snapshot_financial_results as notmain WHERE notmain.snapshot_id = main.id and notmain.is_posted = 1),
            created_at,
            updated_at,
            is_locked
        FROM finance.snapshot as main
        ORDER BY end_of_month DESC
"""

        rows = self._fetch_all(sql, {})
        return [Snapshot.model_validate(row) for row in rows]

    def get_snapshot(self, snapshot_id: int) -> Snapshot | None:
        sql = """

        SELECT
            id, 
            end_of_month,
            groups_count = (SELECT count(*) FROM finance.snapshot_financial_results as notmain WHERE notmain.snapshot_id = main.id),
            posted_count = (SELECT count(*) FROM finance.snapshot_financial_results as notmain WHERE notmain.snapshot_id = main.id and notmain.is_posted = 1),
            created_at,
            updated_at,
            is_locked
        FROM finance.snapshot as main
        WHERE id = :snapshot_id

"""

        row = self._fetch_one(sql, {"snapshot_id": snapshot_id})
        return Snapshot.model_validate(row) if row else None

    def get_results(self, snapshot_id: int) -> list[SnapshotResults]:
        sql = """
        SELECT
            id = main.id,
            snapshot_id = main.snapshot_id,
            group_id = main.group_id,
            group_name = groups.name,
            division_name = divisions.name,
            is_posted = main.is_posted
        FROM finance.snapshot_financial_results AS main
        JOIN finance.dimGroups AS groups ON groups.id = main.group_id
        LEFT JOIN finance.dimDivision AS divisions ON divisions.id = groups.division_id
                WHERE main.snapshot_id = :snapshot_id
"""

        rows = self._fetch_all(sql, {"snapshot_id": snapshot_id})
        return [SnapshotResults.model_validate(row) for row in rows]

    def get_history(self, snapshot_id: int) -> list[SnapshotHistory]:
        sql = """
        SELECT
            id = main.id,
            snapshot_id = main.snapshot_id,
            action_type = main.action_type,
            notes = main.notes,
            user_id = users.id,
            user_name = users.name,
            created_at = main.created_at
        FROM finance.snapshot_history AS main
        LEFT JOIN api.users AS users ON users.id = main.user_id
        WHERE main.snapshot_id = :snapshot_id
"""

        rows = self._fetch_all(sql, {"snapshot_id": snapshot_id})
        return [SnapshotHistory.model_validate(row) for row in rows]

    def save(self, end_of_month: date, user_id: int) -> int:
        sql = """ exec finance.usp_FR_Snapshot_save :end_of_month, :user_id """

        return self._scalar(sql, {"end_of_month": end_of_month, "user_id": user_id})

    def lock(self, snapshot_id: int, user_id: int, note: str) -> None:
        sql = """ exec finance.usp_FR_Snapshot_lock :snapshot_id, :user_id, :note """
        self._execute(
            sql, {"snapshot_id": snapshot_id, "user_id": user_id, "note": note}
        )

    def unlock(self, snapshot_id: int, user_id: int, note: str) -> None:
        sql = """ exec finance.usp_FR_Snapshot_unlock :snapshot_id, :user_id, :note """
        self._execute(
            sql, {"snapshot_id": snapshot_id, "user_id": user_id, "note": note}
        )

    def update(self, snapshot_id: int, user_id: int, note: str) -> None:
        sql = """ exec finance.usp_FR_Snapshot_update :snapshot_id, :user_id, :note """
        self._execute(
            sql, {"snapshot_id": snapshot_id, "user_id": user_id, "note": note}
        )

    def post(self, snapshot_id: int, resault_id: int, is_posted: bool) -> None:
        sql = """
            update finance.snapshot_financial_results set
            is_posted = :is_posted
            WHERE
                snapshot_id = :snapshot_id AND
                id = :resault_id
        """
        self._execute(
            sql,
            {
                "snapshot_id": snapshot_id,
                "resault_id": resault_id,
                "is_posted": is_posted,
            },
        )
