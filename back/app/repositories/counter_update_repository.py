from datetime import date
from typing import Any

from app.config import get_settings
from app.models.counter_update import CounterUpdate
from app.repositories.base import BaseRepository

settings = get_settings()


class CounterUpdateRepository(BaseRepository):
    def get_by_id(self, counter_update_id: int) -> CounterUpdate | None:
        sql = """
            SELECT
                id, 
                start_date,
                end_date,
                id_counter,
                amount,
                auto,
                comment
            FROM Adaugari.dbo.counters_update
            WHERE id = :id
        """
        row = self._fetch_one(sql, {"id": counter_update_id})
        if row is None:
            return None
        return CounterUpdate.model_validate(row)

    def get_all(
        self,
        *,
        cursor_id: int | None = None,
        id_counter: int | None = None,
        auto: bool | None = None,
        start_date_from: date | None = None,
        start_date_to: date | None = None,
    ) -> tuple[list[CounterUpdate], int | None]:
        limit = settings.PAGE_LIMIT

        where = []
        params: dict[str, Any] = {"limit": limit}
        print(cursor_id)
        if cursor_id is not None:
            where.append("id < :cursor_id")
            params["cursor_id"] = cursor_id

        if id_counter is not None:
            where.append("id_counter = :id_counter")
            params["id_counter"] = id_counter

        if auto is not None:
            where.append("auto = :auto")
            params["auto"] = auto

        if start_date_from is not None:
            where.append("start_date >= :start_date_from")
            params["start_date_from"] = start_date_from

        if start_date_to is not None:
            where.append("start_date <= :start_date_to")
            params["start_date_to"] = start_date_to

        where_sql = f"WHERE {' AND '.join(where)}" if where else ""

        sql = f"""
            SELECT TOP (:limit)
                id,
                start_date,
                end_date,
                id_counter,
                amount,
                auto,
                comment
            FROM Adaugari.dbo.counters_update
            {where_sql}
            ORDER BY id DESC
        """

        rows = self._fetch_all(sql, params)
        items = [CounterUpdate.model_validate(row) for row in rows]
        next_cursor = items[-1].id if len(items) == limit else None
        return items, next_cursor
