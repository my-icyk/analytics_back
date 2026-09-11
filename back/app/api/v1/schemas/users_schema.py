from pydantic import BaseModel, ConfigDict, Field


class Base(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserRead(Base):
    id: int
    username: str
    is_admin: bool


class UserUpdate(Base):
    username: str = Field(..., min_length=5, max_length=50)


class MyUser(Base):
    id: int
    username: str
    is_admin: bool
    roles: list[str]
    permissions: list[str]


class UserCreate(Base):
    username: str
    password: str = Field(..., min_length=8, max_length=128)
