from pydantic import BaseModel


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
