import secrets
from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.config import get_settings
from app.core.security import hash_token, verify_password
from app.db.models.auth import User
from app.exceptions.exceptions import (
    InactiveUserError,
    InvalidCredentialsError,
    InvalidSessionError,
)
from app.repositories.auth import SessionRepo
from app.services.common import WriteService

settings = get_settings()


class AuthenticationService(WriteService):
    def __init__(self, session: Session, *, session_repo: SessionRepo):
        super().__init__(session)
        self._sessions = session_repo

    def login(self, username: str, password: str) -> str:
        with self._write():
            user = self._sessions.get_user_for_login(username)

            if user is None or not verify_password(password, user.hashed_password):
                raise InvalidCredentialsError()

            if not user.is_active:
                raise InactiveUserError(user.username)

            token = secrets.token_urlsafe(32)

            # SQL Server DATETIME2 stores no offset. Store UTC consistently.
            now = datetime.now(UTC).replace(tzinfo=None)
            self._sessions.replace(
                user_id=user.id,
                token_hash=hash_token(token),
                created_at=now,
                expires_at=now + settings.SESSION_LIFETIME,
            )

        return token

    def authenticate_user(self, token: str | None) -> User:
        if not token:
            raise InvalidSessionError()

        user = self._sessions.get_active_user(hash_token(token))
        if user is None:
            raise InvalidSessionError()

        return user

    def logout(self, token: str | None) -> None:
        if token:
            with self._write():
                self._sessions.delete_by_token_hash(hash_token(token))
