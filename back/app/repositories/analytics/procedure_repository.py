from app.domains.analytics import Procedure, ProcedureHistory
from app.repositories.base import BaseRepository


class ProcedureRepository(BaseRepository):
    def get_by_id(self, id) -> Procedure | None:
        sql = "SELECT * FROM ProcedureRunList WHERE id = :id"
        row = self._fetch_one_or_none(sql, {"id": id})
        return Procedure.model_validate(row) if row else None

    def get_all(self) -> list[Procedure]:
        sql = "SELECT * FROM ProcedureRunList"
        rows = self._fetch_all(sql)
        return [Procedure.model_validate(row) for row in rows]

    def create(self, name: str, exec_order: int) -> int:
        sql = """
        INSERT INTO ProcedureRunList (name, exec_order, is_active)
        OUTPUT INSERTED.id
        VALUES (:name, :exec_order, 1)

        """
        id = self._scalar(
            sql,
            {
                "name": name,
                "exec_order": exec_order,
            },
        )
        return id

    def update(self, id: int, name: str, exec_order: int, is_active: bool) -> None:
        sql = """
        UPDATE ProcedureRunList SET
            name = :name,
            exec_order = :exec_order,
            is_active = :is_active
        WHERE id = :id
        """
        self._execute(
            sql,
            {
                "id": id,
                "name": name,
                "exec_order": exec_order,
                "is_active": is_active,
            },
        )

    def delete(self, id: int) -> None:
        sql = "DELETE FROM ProcedureRunList WHERE id = :id"
        self._execute(sql, {"id": id})

    def run_by_id(self, name: str) -> None:

        sql = f"exec ProcedureExecutor {name}"
        self._execute(sql, {"name": name})

    def exists_by_name(self, name: str, exclude_id: int | None = None) -> bool:
        return bool(
            self._scalar(
                """
                SELECT CASE WHEN EXISTS (
                    SELECT 1
                    FROM dbo.ProcedureRunList
                    WHERE name = :name
                      AND (:exclude_id IS NULL OR id <> :exclude_id)
                ) THEN 1 ELSE 0 END
                """,
                {"name": name, "exclude_id": exclude_id},
            )
        )

    def get_last_history_by_id(self, procedure_id: int) -> list[ProcedureHistory]:
        sql = """
        SELECT TOP 10 * FROM ProcedureRunHistory
        WHERE procedure_id = :procedure_id
        ORDER BY
            start_at DESC
        """
        row = self._fetch_all(sql, {"procedure_id": procedure_id})
        return [ProcedureHistory.model_validate(r) for r in row] if row else []
