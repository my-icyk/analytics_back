from app.domains.permission import Permission
from app.repositories.base import BaseRepository


class RolePermissionRepository(BaseRepository):
    def assign(self, role_id: int, permission_id: int) -> None:
        sql = """
            INSERT INTO api.role_permissions (role_id, permission_id)
            VALUES (:role_id, :permission_id)
        """
        self._execute(sql, {"role_id": role_id, "permission_id": permission_id})

    def revoke(self, role_id: int, permission_id: int) -> None:
        sql = """
            DELETE FROM api.role_permissions
            WHERE
                role_id = :role_id AND
                permission_id = :permission_id
        """
        self._execute(sql, {"role_id": role_id, "permission_id": permission_id})

    def get_permissions_by_role_id(self, role_id: int) -> list[Permission]:
        sql = """
            SELECT p.*
            FROM api.role_permissions AS rp
            JOIN api.permissions AS p ON rp.permission_id = p.id
            WHERE
                rp.role_id = :role_id
        """
        rows = self._fetch_all(sql, {"role_id": role_id})
        return [Permission.model_validate(row) for row in rows]

    def role_has_permission(self, role_id: int, permission_id: int) -> bool:
        sql = """
            SELECT TOP 1 1
            FROM api.role_permissions
            WHERE
                role_id = :role_id AND
                permission_id = :permission_id
        """
        row = self._fetch_one_or_none(
            sql, {"role_id": role_id, "permission_id": permission_id}
        )
        return row is not None
