import hashlib
import uuid
from datetime import UTC, datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import get_settings
from app.exceptions.exceptions import PasswordMismatchError

settings = get_settings()

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__memory_cost=65536,
    argon2__time_cost=3,
    argon2__parallelism=4,
    argon2__type="id",
)

# Password constraints
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 128


def validate_password_strength(password: str) -> None:
    """
    Validate password meets security requirements.
    Raises ValueError if invalid.
    """
    if len(password) < MIN_PASSWORD_LENGTH:
        raise ValueError(
            f"Password must be at least {MIN_PASSWORD_LENGTH} characters long"
        )

    if len(password) > MAX_PASSWORD_LENGTH:
        raise ValueError(f"Password is too long (max {MAX_PASSWORD_LENGTH} characters)")

    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)

    if not (has_upper and has_lower and has_digit):
        raise PasswordMismatchError()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password using Argon2."""
    return pwd_context.hash(password)


def needs_rehash(hashed_password: str) -> bool:
    """Check if a password hash needs to be updated."""
    return pwd_context.needs_update(hashed_password)


# ---------------------------------------------------------------------------
# Access tokens
# ---------------------------------------------------------------------------
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Create a short-lived JWT access token. `type: access` prevents a refresh
    token from being accepted anywhere an access token is expected.
    """
    to_encode = data.copy()

    expire = datetime.now(UTC) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update(
        {
            "exp": expire,
            "iat": datetime.now(UTC),
            "type": "access",
        }
    )

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    """Decode + validate an access token. Returns None if invalid, expired, or wrong type."""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    except JWTError:
        return None

    if payload.get("type") != "access":
        return None

    return payload


# ---------------------------------------------------------------------------
# Refresh tokens
# ---------------------------------------------------------------------------
def create_refresh_token(data: dict) -> tuple[str, str, datetime]:
    """
    Create a long-lived refresh token.

    Returns (raw_token, token_hash, expires_at) — the raw token goes to the
    client, the hash is what you store in the `refresh_tokens` table.
    Never store the raw token; a stolen DB row shouldn't be usable as a
    live credential.
    """
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    jti = str(uuid.uuid4())

    to_encode.update(
        {
            "exp": expire,
            "iat": datetime.now(UTC),
            "type": "refresh",
            "jti": jti,
        }
    )

    raw_token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    token_hash = hash_token(raw_token)

    return raw_token, token_hash, expire


def decode_refresh_token(token: str) -> dict | None:
    """Decode + validate a refresh token. Returns None if invalid, expired, or wrong type."""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    except JWTError:
        return None

    if payload.get("type") != "refresh":
        return None

    return payload


def hash_token(raw_token: str) -> str:
    """
    SHA-256 hash of a raw token, for DB storage/lookup. Not a password hash
    (no need for Argon2 here — the token itself already has ~256 bits of
    entropy from the JWT signature+claims, we just need a fast, deterministic
    lookup key, not brute-force resistance).
    """
    return hashlib.sha256(raw_token.encode()).hexdigest()
