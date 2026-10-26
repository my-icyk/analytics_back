from app.domains.permission import Permission
from app.repositories.base import BaseRepository


class PermissionRepository(BaseRepository):
    def get_all(self) -> list[Permission]:
        sql = """
            SELECT
                id,
                name
            FROM api.permissions
            ORDER BY
                name
        """

        rows = self._fetch_all(sql)
        return [Permission.model_validate(row) for row in rows]

    def get_existing_ids(self, ids: list[int]) -> set[int]:
        if not ids:
            return set()
        rows = self._fetch_all(
            "SELECT id FROM api.permissions WHERE id IN :ids",
            {"ids": ids},
        )
        return {row["id"] for row in rows}
