"""
User repository — every statement is explicit, hand-written SQL.
`OUTPUT INSERTED.*` / `OUTPUT INSERTED.*` on INSERT/UPDATE lets us get the
full row (including DB-generated id, created_at, updated_at) back in one
round trip instead of a separate SELECT.
"""

from app.domains.user import User
from app.repositories.base import BaseRepository


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

    def create(self, username: str, hashed_password: str) -> User:
        sql = """
            INSERT INTO api.users (username, hashed_password)
            OUTPUT INSERTED.*
            VALUES (:username, :hashed_password)
        """
        row = self._fetch_one_or_none(
            sql,
            {
                "username": username,
                "hashed_password": hashed_password,
            },
        )
        assert row is not None, "INSERT with OUTPUT should always return a row"
        return User.model_validate(row)

    def update_user(self, user_id: int, username: str) -> User:

        params = {"user_id": user_id, "username": username}

        sql = """
            UPDATE api.users SET
                username = :username
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
        rows = self._fetch_all(sql, {})
        return [User.model_validate(row) for row in rows]

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
