from app.models.permission import Permission
from app.repositories.base import BaseRepository


class RolePermissionRepository(BaseRepository):
    def create(self, role_id: int, permission_id: int) -> None:
        sql = """
            INSERT INTO api.role_permissions(role_id, permission_id)
            VALUES (:role_id, :permission_id)
        """
        self._execute(sql, {"role_id": role_id, "permission_id": permission_id})

    def delete(self, role_id: int, permission_id: int) -> None:
        sql = """
            DELETE FROM api.role_permissions
            WHERE role_id = :role_id AND permission_id = :permission_id
        """
        self._execute(sql, {"role_id": role_id, "permission_id": permission_id})

    def get_permissions_by_role_id(self, role_id: int) -> list[Permission]:
        sql = """
            SELECT p.id, p.name
            FROM api.role_permissions AS rp
            JOIN api.permissions AS p ON rp.permission_id = p.id
            WHERE role_id = :role_id
        """
        rows = self._fetch_all(sql, {"role_id": role_id})
        return [Permission.model_validate(row) for row in rows]

    def exists(self, role_id: int, permission_id: int) -> bool:
        sql = """
            SELECT 1
            FROM api.role_permissions
            WHERE role_id = :role_id AND permission_id = :permission_id
        """
        row = self._fetch_one(sql, {"role_id": role_id, "permission_id": permission_id})
        return row is not None
