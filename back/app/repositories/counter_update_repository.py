from datetime import date

from app.config import get_settings
from app.domains.counter_update import CounterExceptions, Counters
from app.repositories.base import BaseRepository

settings = get_settings()


class CounterUpdateRepository(BaseRepository):
    def get_by_id(self, counter_update_id: int) -> CounterExceptions | None:
        sql = """
            SELECT 
                main.id,
                main.counter_id,
                main.valid_from,
                main.valid_to,
                main.visitors,
                main.is_auto,
                main.reason,
                created_by = users.username,
                main.created_at,
                main.updated_at
            FROM testing_db.params.counter_exceptions AS main
            LEFT JOIN testing_db.api.users ON users.id = main.created_by_user_id
            WHERE
                main.id = :counter_update_id
            ORDER BY
                main.updated_at DESC
        """
        row = self._fetch_one_or_none(sql, {"counter_update_id": counter_update_id})
        return CounterExceptions.model_validate(row) if row else None

    def create(
        self,
        *,
        counter_id: int,
        valid_from: date,
        valid_to: date,
        is_auto: bool,
        visitors: int,
        reason: str | None = None,
        created_by_user_id: int,
    ) -> None:
        sql = """
            INSERT INTO testing_db.params.counter_exceptions (
                counter_id,
                valid_from,
                valid_to,
                visitors,
                is_auto,
                reason,
                created_by_user_id
            ) 
            VALUES (
                :counter_id,
                :valid_from,
                :valid_to,
                :visitors,
                :is_auto,
                :reason,
                :created_by_user_id
            );
        """
        params = {
            "counter_id": counter_id,
            "valid_from": valid_from,
            "valid_to": valid_to,
            "visitors": visitors,
            "is_auto": is_auto,
            "reason": reason,
            "created_by_user_id": created_by_user_id,
        }
        self._execute(sql, params)

    def update(
        self,
        *,
        exception_id: int,
        counter_id: int,
        valid_from: date,
        valid_to: date,
        visitors: int,
        is_auto: bool,
        reason: str | None = None,
    ) -> None:
        sql = """
            UPDATE testing_db.params.counter_exceptions
            SET
                counter_id = :counter_id,
                valid_from = :valid_from,
                valid_to = :valid_to,
                visitors = :visitors,
                is_auto = :is_auto,
                reason = :reason,
                updated_at = GETDATE()
            WHERE id = :exception_id;
        """
        params = {
            "exception_id": exception_id,
            "counter_id": counter_id,
            "valid_from": valid_from,
            "valid_to": valid_to,
            "visitors": visitors,
            "is_auto": is_auto,
            "reason": reason,
        }
        self._execute(sql, params)

    def delete(
        self,
        *,
        exception_id: int,
    ) -> None:
        sql = """
            DELETE FROM testing_db.params.counter_exceptions
            WHERE id = :exception_id;
        """
        params = {
            "exception_id": exception_id,
        }
        self._execute(sql, params)

    def get_counters(self) -> list[Counters]:
        sql = """
            SELECT
                id = counter_id,
                exception_count = COUNT(*),
                last_change = MAX(updated_at)
            FROM testing_db.params.counter_exceptions
            GROUP BY
                counter_id
            ORDER BY
                MAX(updated_at) DESC
        """

        rows = self._fetch_all(sql, {})
        return [Counters.model_validate(row) for row in rows]

    def get_by_counter_id(self, counter_id: int) -> list[CounterExceptions]:
        sql = """
            SELECT 
                main.id,
                main.counter_id,
                main.valid_from,
                main.valid_to,
                main.visitors,
                main.is_auto,
                main.reason,
                created_by = users.username,
                main.created_at,
                main.updated_at
            FROM testing_db.params.counter_exceptions AS main
            LEFT JOIN testing_db.api.users ON users.id = main.created_by_user_id
            WHERE
                counter_id = :counter_id
            ORDER BY
                main.updated_at DESC
        """

        params = {
            "counter_id": counter_id,
        }
        rows = self._fetch_all(sql, params)
        return [CounterExceptions.model_validate(row) for row in rows]
