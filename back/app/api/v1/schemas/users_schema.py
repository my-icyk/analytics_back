from pydantic import BaseModel, Field


class UserRead(BaseModel):
    id: int
    username: str
    is_admin: bool


class UserUpdate(BaseModel):
    username: str = Field(..., min_length=5, max_length=50)


class MyUser(BaseModel):
    user: UserRead
    permissions: list[str] = []


class UserCreate(BaseModel):
    username: str
    password: str = Field(..., min_length=8, max_length=128)
