"""
Auth service — orchestrates UserRepository + RefreshTokenRepository +
security.py to implement login, refresh-token rotation, and logout.
"""

from datetime import datetime

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
    decode_refresh_token,
    hash_token,
    verify_password,
)
from app.exceptions.exceptions import (
    InactiveUserError,
    InvalidCredentialsError,
    InvalidTokenError,
)
from app.repositories.authentication_repository import AuthenticationRepository
from app.repositories.user_repository import UserRepository


class AuthenticationService:
    def __init__(self, user_repo: UserRepository, auth_repo: AuthenticationRepository):
        self.user_repo = user_repo
        self.auth_repo = auth_repo

    # -----------------------------------------------------------------
    def login(self, name: str, password: str) -> tuple[str, str, datetime]:
        """Returns (access_token, raw_refresh_token, refresh_expires_at)."""
        user = self.user_repo.get_by_username(name)

        if user is None or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError()

        if not user.is_active:
            raise InactiveUserError(user.id)

        access_token = create_access_token({"sub": str(user.id)})
        raw_refresh, refresh_hash, expires_at = create_refresh_token(
            {"sub": str(user.id)}
        )
        self.auth_repo.create(user.id, refresh_hash, expires_at)

        return access_token, raw_refresh, expires_at

    # -----------------------------------------------------------------
    def refresh(self, raw_refresh_token: str) -> tuple[str, str, datetime]:
        """
        Validates + rotates a refresh token. Returns a brand new
        (access_token, raw_refresh_token, refresh_expires_at) triple.
        The old refresh token is revoked as part of this call.
        """
        payload = decode_refresh_token(raw_refresh_token)
        if payload is None:
            raise InvalidTokenError()

        token_hash = hash_token(raw_refresh_token)
        stored = self.auth_repo.get_by_hash(token_hash)

        if stored is None:
            raise InvalidTokenError()

        if stored["revoked_at"] is not None:
            # This token was already used/rotated once before. Seeing it
            # again means either a replay or a stolen token being reused —
            # in both cases, the safest move is to kill every active
            # refresh token for this user and force a fresh login.
            self.auth_repo.revoke_all_for_user(stored["user_id"])
            raise InvalidTokenError()

        user = self.user_repo.get_by_id(stored["user_id"])
        if user is None or not user.is_active:
            raise InvalidTokenError()

        access_token = create_access_token({"sub": str(user.id)})
        new_raw_refresh, new_hash, new_expires_at = create_refresh_token(
            {"sub": str(user.id)}
        )
        new_row = self.auth_repo.create(user.id, new_hash, new_expires_at)
        self.auth_repo.revoke(stored["id"], replaced_by=new_row["id"])

        return access_token, new_raw_refresh, new_expires_at

    # -----------------------------------------------------------------
    def logout(self, raw_refresh_token: str) -> None:
        token_hash = hash_token(raw_refresh_token)
        stored = self.auth_repo.get_by_hash(token_hash)
        if stored is not None and stored["revoked_at"] is None:
            self.auth_repo.revoke(stored["id"])

    def authenticate_user(self, token: str) -> int:
        payload = decode_access_token(token)
        if payload is None:
            raise InvalidTokenError()

        user_id = payload.get("sub")
        if user_id is None:
            raise InvalidTokenError()

        return user_id
