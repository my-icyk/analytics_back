"""
User repository — every statement is explicit, hand-written SQL.
`OUTPUT INSERTED.*` / `OUTPUT INSERTED.*` on INSERT/UPDATE lets us get the
full row (including DB-generated id, created_at, updated_at) back in one
round trip instead of a separate SELECT.
"""

from app.exceptions.exceptions import NotFoundError
from app.models.role import Role
from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    def get_by_id(self, user_id: int) -> User | None:
        sql = """
            SELECT id, username, role, is_active, created_at, is_admin, hashed_password
            FROM api.users
            WHERE id = :id
        """
        row = self._fetch_one(sql, {"id": user_id})
        if row is None:
            return None
        return User.model_validate(row)

    def get_by_username(self, username: str) -> User | None:
        sql = """
            SELECT id, username, role, is_active, created_at, is_admin, hashed_password
            FROM api.users
            WHERE username = :username
        """
        row = self._fetch_one(sql, {"username": username})
        if row is None:
            return None
        return User.model_validate(row)

    def delete(self, user_id: int) -> None:
        sql = """
            DELETE FROM api.users
            WHERE id = :id
        """
        self._execute(sql, {"id": user_id})

    def create(
        self, username: str, hashed_password: str, is_admin: bool = False
    ) -> User:
        sql = """
            INSERT INTO api.users (username, hashed_password, is_admin)
            OUTPUT INSERTED.id, INSERTED.username, INSERTED.role, INSERTED.is_active,
                   INSERTED.created_at, INSERTED.is_admin, INSERTED.hashed_password
            VALUES (:username, :hashed_password, :is_admin)
        """
        row = self._fetch_one(
            sql,
            {
                "username": username,
                "hashed_password": hashed_password,
                "is_admin": is_admin,
            },
        )
        return User.model_validate(row)

    def assign_role_to_user(self, user_id: int, role_id: int) -> None:
        sql = """
            INSERT INTO api.user_roles (user_id, role_id)
            VALUES (:user_id, :role_id)
        """
        self._execute(sql, {"user_id": user_id, "role_id": role_id})

    def remove_role_from_user(self, user_id: int, role_id: int) -> None:
        sql = """
            DELETE FROM api.user_roles
            WHERE user_id = :user_id AND role_id = :role_id
        """
        self._execute(sql, {"user_id": user_id, "role_id": role_id})

    def get_roles_by_user_id(self, user_id: int) -> list[Role] | None:
        sql = """
            SELECT r.id, r.name, r.description, r.created_at
            FROM api.roles r
            JOIN api.user_roles ur ON r.id = ur.role_id
            WHERE ur.user_id = :user_id
        """
        rows = self._fetch_all(sql, {"user_id": user_id})
        if not rows:
            return None
        return [Role.model_validate(row) for row in rows]

    def get_user_permissions(self, user_id: int) -> list[str]:
        sql = """
            SELECT DISTINCT p.name
            FROM api.permissions p
            JOIN api.role_permissions rp ON p.id = rp.permission_id
            JOIN api.user_roles ur ON rp.role_id = ur.role_id
            WHERE ur.user_id = :user_id
        """
        rows = self._fetch_all(sql, {"user_id": user_id})
        return [row["name"] for row in rows]

    def update_user(self, user_id: int, username: str, is_admin: bool) -> User:

        params = {"user_id": user_id, "username": username, "is_admin": is_admin}

        sql = """
            UPDATE api.users
            SET username = :username,
                is_admin = :is_admin
            OUTPUT INSERTED.id, INSERTED.username, INSERTED.role, INSERTED.is_active,
                   INSERTED.created_at, INSERTED.is_admin, INSERTED.hashed_password
            WHERE id = :user_id
        """

        row = self._fetch_one(sql, params)
        if row is None:
            raise NotFoundError("User", "id", user_id)
        return User.model_validate(row)

    def get_all_users(self) -> list[User]:
        sql = """
            SELECT id, username, role, is_active, created_at, is_admin, hashed_password
            FROM api.users
        """
        rows = self._fetch_all(sql, {})
        return [User.model_validate(row) for row in rows]
