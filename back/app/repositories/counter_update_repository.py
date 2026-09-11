from datetime import date
from typing import Any

from app.config import get_settings
from app.domains.counter_update import CounterUpdate
from app.repositories.base import BaseRepository

settings = get_settings()


class CounterUpdateRepository(BaseRepository):
    def get_by_id(self, counter_update_id: int) -> CounterUpdate | None:
        sql = """
            SELECT *
            FROM Adaugari.dbo.counters_update
            WHERE id = :id
        """
        row = self._fetch_one_or_none(sql, {"id": counter_update_id})
        return CounterUpdate.model_validate(row) if row else None

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
            SELECT TOP (:limit) *
            FROM Adaugari.dbo.counters_update
            {where_sql}
            ORDER BY id DESC
        """

        rows = self._fetch_all(sql, params)
        items = [CounterUpdate.model_validate(row) for row in rows]
        next_cursor = items[-1].id if len(items) == limit else None
        return items, next_cursor

    def create(
        self,
        *,
        start_date: date,
        end_date: date,
        id_counter: int,
        amount: int,
        auto: bool,
        comment: str | None = None,
    ) -> None:
        sql = """
            INSERT INTO Adaugari.dbo.counters_update (
                start_date,
                end_date,
                id_counter,
                amount,
                auto,
                comment
            ) 
            VALUES (
                :start_date,
                :end_date,
                :id_counter,
                :amount,
                :auto,
                :comment
            );
        """
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "id_counter": id_counter,
            "amount": amount,
            "auto": auto,
            "comment": comment,
        }
        self._execute(sql, params)

    def update(
        self,
        *,
        counter_update_id: int,
        start_date: date,
        end_date: date,
        id_counter: int,
        amount: int,
        auto: bool,
        comment: str | None = None,
    ) -> None:
        sql = """
            UPDATE Adaugari.dbo.counters_update
            SET
                start_date = :start_date,
                end_date = :end_date,
                id_counter = :id_counter,
                amount = :amount,
                auto = :auto,
                comment = :comment
            WHERE id = :counter_update_id;
        """
        params = {
            "counter_update_id": counter_update_id,
            "start_date": start_date,
            "end_date": end_date,
            "id_counter": id_counter,
            "amount": amount,
            "auto": auto,
            "comment": comment,
        }
        self._execute(sql, params)

    def delete(
        self,
        *,
        counter_update_id: int,
    ) -> None:
        sql = """
            DELETE FROM Adaugari.dbo.counters_update
            WHERE id = :counter_update_id;
        """
        params = {
            "counter_update_id": counter_update_id,
        }
        self._execute(sql, params)
