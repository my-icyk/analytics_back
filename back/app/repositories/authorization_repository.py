from app.repositories.base import BaseRepository


class AuthorizationRepository(BaseRepository):
    def user_has_permission(self, user_id: int, permission_name: str) -> bool:
        query = """
                SELECT 1
                FROM api.user_roles ur
                JOIN api.role_permissions rp ON rp.role_id = ur.role_id
                JOIN api.permissions p ON p.id = rp.permission_id
                WHERE ur.user_id = :user_id AND p.name = :permission_name
        """
        result = self._fetch_one_or_none(
            query, {"user_id": user_id, "permission_name": permission_name}
        )
        return result is not None

    def user_is_admin(self, user_id: int) -> bool:
        query = """
            SELECT 1
            FROM api.users
            WHERE id = :user_id
              AND is_admin = 1
        """

        result = self._fetch_one_or_none(
            query,
            {"user_id": user_id},
        )

        return result is not None
