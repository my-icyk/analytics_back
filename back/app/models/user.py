from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    is_active: bool
    is_admin: bool
    hashed_password: str


class UserCreate(BaseModel):
    username: str
    password: str
