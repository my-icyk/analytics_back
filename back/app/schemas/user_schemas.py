from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(BaseModel):
    username: str
    password: str
    is_admin: bool = False


class UserRead(BaseModel):
    id: int
    username: str
    is_admin: bool


class UserRegister(BaseModel):
    username: str
    password: str = Field(..., min_length=8, max_length=128)
