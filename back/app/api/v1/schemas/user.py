from datetime import datetime

from pydantic import Field

from app.api.v1.schemas.finance import Base


class UserRead(Base):
    id: int
    username: str
    is_admin: bool
    is_active: bool
    name: str
    email: str | None = None


class UserUpdate(Base):
    username: str = Field(..., min_length=5, max_length=50)
    email: str | None = None
    is_active: bool
    name: str


class MyUser(Base):
    id: int
    username: str
    is_admin: bool
    created_at: datetime
    email: str | None = None
    name: str
    roles: list[str]
    permissions: list[str]


class UserCreate(Base):
    username: str
    email: str | None = None
    password: str = Field(..., min_length=8, max_length=128)
    name: str


class PasswordChange(Base):
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=128)


class PasswordReset(Base):
    new_password: str = Field(..., min_length=8, max_length=128)
