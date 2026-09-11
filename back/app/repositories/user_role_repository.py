from app.domains.role import Role
from app.repositories.base import BaseRepository


class UserRoleRepository(BaseRepository):
    def assign(self, user_id: int, role_id: int) -> None:
        sql = """
            INSERT INTO api.user_roles (user_id, role_id)
            VALUES (:user_id, :role_id)
        """
        self._execute(sql, {"user_id": user_id, "role_id": role_id})

    def revoke(self, user_id: int, role_id: int) -> None:
        sql = """
            DELETE FROM api.user_roles
            WHERE user_id = :user_id AND role_id = :role_id
        """
        self._execute(sql, {"user_id": user_id, "role_id": role_id})

    def get_roles_by_user_id(self, user_id: int) -> list[Role]:
        sql = """
            SELECT r.*
            FROM api.roles r
            JOIN api.user_roles ur ON ur.role_id = r.id
            WHERE ur.user_id = :user_id
        """
        rows = self._fetch_all(sql, {"user_id": user_id})
        return [Role.model_validate(row) for row in rows]

    def user_has_role(self, user_id: int, role_id: int) -> bool:
        sql = """
            SELECT 1
            FROM api.user_roles
            WHERE user_id = :user_id AND role_id = :role_id
        """
        row = self._fetch_one_or_none(sql, {"user_id": user_id, "role_id": role_id})
        return row is not None
