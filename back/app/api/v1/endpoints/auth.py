from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.config import get_settings
from app.core.security import (
    create_access_token,
    get_password_hash,
    needs_rehash,
    verify_password,
)
from app.db.database import get_db
from app.exceptions.exceptions import AlreadyExistsError
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import Token
from app.schemas.user_schemas import UserCreate, UserRead

router = APIRouter()
settings = get_settings()


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Register a new user. Only accessible by admin users.
    """

    if UserRepository(db).get_by_username(user_data.username):
        raise AlreadyExistsError("User", "username", user_data.username)

    repo = UserRepository(db)

    if repo.get_by_username(user_data.username):
        raise AlreadyExistsError("User", "username", user_data.username)

    user = repo.create(user_data.username, get_password_hash(user_data.password))
    return user


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Login endpoint. Returns JWT access token.
    Token expires after ACCESS_TOKEN_EXPIRE_MINUTES (from config).
    """
    user = UserRepository(db).get_by_username(form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User account is disabled"
        )

    # Check if password hash needs updating (e.g., from bcrypt to argon2)
    if needs_rehash(user.hashed_password):
        user.hashed_password = get_password_hash(form_data.password)
        db.commit()

    # Create access token with configured expiration time
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}
