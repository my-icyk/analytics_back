from app.models.permission import Permission
from app.repositories.base import BaseRepository


class PermissionRepository(BaseRepository):
    def get_by_id(self, permission_id: int) -> Permission | None:
        sql = """
            SELECT id, name
            FROM api.permissions
            WHERE id = :id
        """
        row = self._fetch_one(sql, {"id": permission_id})
        if row is None:
            return None
        return Permission.model_validate(row)

    def get_by_name(self, name: str) -> Permission | None:
        sql = """
            SELECT id, name
            FROM api.permissions
            WHERE name = :name
        """
        row = self._fetch_one(sql, {"name": name})
        if row is None:
            return None
        return Permission.model_validate(row)

    def get_all(self) -> list[Permission]:
        sql = """
            SELECT id, name
            FROM api.permissions
        """
        # TODO: Consider adding pagination to this method if the number of permissions grows large
        rows = self._fetch_all(sql, {})
        return [Permission.model_validate(row) for row in rows]
