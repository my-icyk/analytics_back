from datetime import datetime

from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from app.db.models.auth import User, UserSession


class SessionRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_user_for_login(self, username: str) -> User | None:
        stmt = (
            select(User)
            .where(User.username == username)
            .with_hint(User, "WITH (UPDLOCK)", dialect_name="mssql")
        )
        return self._session.scalar(stmt)

    def replace(
        self,
        user_id: int,
        token_hash: str,
        created_at: datetime,
        expires_at: datetime,
    ) -> None:
        row = self._session.get(UserSession, user_id)
        if row is None:
            row = UserSession(user_id=user_id)
            self._session.add(row)

        row.token_hash = token_hash
        row.created_at = created_at
        row.expires_at = expires_at

    def get_active_user(self, token_hash: str) -> User | None:
        stmt = (
            select(User)
            .join(UserSession, UserSession.user_id == User.id)
            .where(
                UserSession.token_hash == token_hash,
                UserSession.expires_at > func.sysutcdatetime(),
                User.is_active == True,  # noqa: E712
            )
        )
        return self._session.scalar(stmt)

    def delete_by_token_hash(self, token_hash: str) -> None:
        self._session.execute(
            delete(UserSession).where(UserSession.token_hash == token_hash)
        )

    def delete_by_user_id(self, user_id: int) -> None:
        self._session.execute(delete(UserSession).where(UserSession.user_id == user_id))
