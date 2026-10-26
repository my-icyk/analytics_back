from app.domains.permission import Permission
from app.repositories.base import BaseRepository


class PermissionRepository(BaseRepository):
    def get_all(self) -> list[Permission]:
        sql = """
            SELECT *
            FROM api.permissions
        """

        rows = self._fetch_all(sql, {})
        return [Permission.model_validate(row) for row in rows]
