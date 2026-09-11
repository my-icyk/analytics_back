from app.domains.permission import Permission
from app.repositories.base import BaseRepository


class PermissionRepository(BaseRepository):
    def get_by_id(self, permission_id: int) -> Permission | None:
        sql = """
            SELECT *
            FROM api.permissions
            WHERE id = :id
        """
        row = self._fetch_one_or_none(sql, {"id": permission_id})

        return Permission.model_validate(row) if row is not None else None

    def get_by_name(self, name: str) -> Permission | None:
        sql = """
            SELECT *
            FROM api.permissions
            WHERE name = :name
        """
        row = self._fetch_one_or_none(sql, {"name": name})
        return Permission.model_validate(row) if row is not None else None

    def get_all(self) -> list[Permission]:
        sql = """
            SELECT *
            FROM api.permissions
        """

        rows = self._fetch_all(sql, {})
        return [Permission.model_validate(row) for row in rows]
