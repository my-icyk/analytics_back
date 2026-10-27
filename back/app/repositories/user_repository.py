"""
User repository — every statement is explicit, hand-written SQL.
`OUTPUT INSERTED.*` / `OUTPUT INSERTED.*` on INSERT/UPDATE lets us get the
full row (including DB-generated id, created_at, updated_at) back in one
round trip instead of a separate SELECT.
"""

from app.domains.user import User
from app.repositories.base import BaseRepository, LookupObjects, LookupResponse


class UserRepository(BaseRepository):
    def get_by_id(self, user_id: int) -> User | None:
        sql = """
            SELECT *
            FROM api.users
            WHERE id = :id
        """
        row = self._fetch_one_or_none(sql, {"id": user_id})

        return User.model_validate(row) if row is not None else None

    def get_by_username(self, username: str) -> User | None:
        sql = """
            SELECT *
            FROM api.users
            WHERE username = :username
        """
        row = self._fetch_one_or_none(sql, {"username": username})

        return User.model_validate(row) if row is not None else None

    def delete(self, user_id: int) -> None:
        sql = """
            DELETE FROM api.users
            WHERE id = :id
        """
        self._execute(sql, {"id": user_id})

    def create(
        self, username: str, hashed_password: str, name: str, email: str | None = None
    ) -> User:
        sql = """
            INSERT INTO api.users (username, hashed_password, name, email)
            OUTPUT INSERTED.*
            VALUES (:username, :hashed_password, :name, :email)
        """
        row = self._fetch_one_or_none(
            sql,
            {
                "username": username,
                "hashed_password": hashed_password,
                "name": name,
                "email": email,
            },
        )
        assert row is not None, "INSERT with OUTPUT should always return a row"
        return User.model_validate(row)

    def update_user(
        self, user_id: int, username: str, email: str | None, is_active: bool, name: str
    ) -> User:

        params = {
            "user_id": user_id,
            "username": username,
            "email": email,
            "is_active": is_active,
            "name": name,
        }

        sql = """
            UPDATE api.users SET
                username = :username,
                email = :email,
                is_active = :is_active,
                name = :name
            OUTPUT INSERTED.*
            WHERE id = :user_id
        """

        row = self._fetch_one_or_none(sql, params)
        assert row is not None, "UPDATE with OUTPUT should always return a row"
        return User.model_validate(row)

    def get_all_users(self) -> list[User]:
        sql = """
            SELECT *
            FROM api.users
        """
        rows = self._fetch_all(sql)
        return [User.model_validate(row) for row in rows]

    def lookup_users(self, search: str) -> list[LookupResponse]:
        rows = self._lookup(LookupObjects.USERS, search)
        return rows

    def set_admin(self, user_id: int) -> User:
        sql = """
            UPDATE api.users SET
                is_admin = 1
            OUTPUT INSERTED.*
            WHERE id = :user_id
        """
        row = self._update(sql, {"user_id": user_id})

        return User.model_validate(row)

    def revoke_admin(self, user_id: int) -> User:
        sql = """
            UPDATE api.users SET
                is_admin = 0
            OUTPUT INSERTED.*
            WHERE id = :user_id
        """
        row = self._update(sql, {"user_id": user_id})
        return User.model_validate(row)

    def assign_roles(
        self,
        user_id: int,
        roles_ids: list[int],
    ) -> None:
        self._execute(
            "DELETE FROM api.user_roles WHERE user_id = :user_id",
            {"user_id": user_id},
        )

        if not roles_ids:
            return

        add_sql = """
            INSERT INTO api.user_roles (user_id, role_id)
            SELECT :user_id, id
            FROM api.roles
            WHERE id IN :roles_ids
            """
        self._execute(
            add_sql,
            {"user_id": user_id, "roles_ids": roles_ids},
        )
