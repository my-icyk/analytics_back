"""
Refresh token repository — issuing, looking up, and revoking refresh tokens.
Only ever stores/queries the SHA-256 hash of a token, never the raw value.
"""

from datetime import datetime

from app.repositories.base import BaseRepository


class AuthenticationRepository(BaseRepository):
    def create(
        self, user_id: int, token_hash: str, expires_at: datetime
    ) -> dict | None:
        sql = """
            INSERT INTO api.refresh_tokens (user_id, token_hash, expires_at)
            OUTPUT INSERTED.id, INSERTED.user_id, INSERTED.token_hash,
                   INSERTED.expires_at, INSERTED.created_at,
                   INSERTED.revoked_at, INSERTED.replaced_by
            VALUES (:user_id, :token_hash, :expires_at)
        """
        return self._fetch_one_or_none(
            sql,
            {"user_id": user_id, "token_hash": token_hash, "expires_at": expires_at},
        )

    def get_by_hash(self, token_hash: str) -> dict | None:
        sql = """
            SELECT id, user_id, token_hash, expires_at, created_at, revoked_at, replaced_by
            FROM api.refresh_tokens
            WHERE token_hash = :token_hash
        """
        return self._fetch_one_or_none(sql, {"token_hash": token_hash})

    def revoke(self, token_id: int, replaced_by: int | None = None) -> None:
        sql = """
            UPDATE api.refresh_tokens
            SET revoked_at = SYSUTCDATETIME(), replaced_by = :replaced_by
            WHERE id = :id
        """
        self._execute(sql, {"id": token_id, "replaced_by": replaced_by})

    def revoke_all_for_user(self, user_id: int) -> None:
        """Used on reuse-detection (possible token theft) and on 'log out everywhere'."""
        sql = """
            UPDATE api.refresh_tokens
            SET revoked_at = SYSUTCDATETIME()
            WHERE user_id = :user_id AND revoked_at IS NULL
        """
        self._execute(sql, {"user_id": user_id})
