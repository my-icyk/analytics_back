import hashlib

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


def hash_token(raw_token: str) -> str:
    """
    SHA-256 hash of a raw token, for DB storage/lookup. Not a password hash
    (no need for Argon2 here — the token itself already has ~256 bits of
    entropy from the JWT signature+claims, we just need a fast, deterministic
    lookup key, not brute-force resistance).
    """
    return hashlib.sha256(raw_token.encode()).hexdigest()
