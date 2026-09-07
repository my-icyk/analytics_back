from app.models.role import Role
from app.models.user import User
from app.repositories.base import BaseRepository


class RoleRepository(BaseRepository):
    def get_all(self) -> list[Role]:
        sql = """
            SELECT id, name, description, created_at
            FROM api.roles
        """
        rows = self._fetch_all(sql, {})
        return [Role.model_validate(row) for row in rows]

    def get_by_id(self, role_id: int) -> Role | None:
        sql = """
            SELECT id, name, description, created_at
            FROM api.roles
            WHERE id = :id
        """
        row = self._fetch_one(sql, {"id": role_id})
        if row is None:
            return None
        return Role.model_validate(row)

    def get_by_name(self, name: str) -> Role | None:
        sql = """
            SELECT id, name, description, created_at
            FROM api.roles
            WHERE name = :name
        """
        row = self._fetch_one(sql, {"name": name})
        if row is None:
            return None
        return Role.model_validate(row)

    def create(self, name: str, description: str | None = None) -> Role:
        sql = """
            INSERT INTO api.roles (name, description)
            OUTPUT INSERTED.id, INSERTED.name, INSERTED.description, INSERTED.created_at
            VALUES (:name, :description)
        """
        row = self._fetch_one(sql, {"name": name, "description": description})
        return Role.model_validate(row)

    def get_users_by_role_id(self, role_id: int) -> list[User] | None:
        sql = """
            SELECT u.id, u.username, u.role, u.is_active, u.created_at
            FROM api.users u
            JOIN api.user_roles ur ON u.id = ur.user_id
            WHERE ur.role_id = :role_id
        """
        rows = self._fetch_all(sql, {"role_id": role_id})
        if not rows:
            return None
        return [User.model_validate(row) for row in rows]
