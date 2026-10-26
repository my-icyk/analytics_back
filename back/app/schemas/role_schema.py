from datetime import datetime

from pydantic import BaseModel


class RoleRead(BaseModel):
    id: int
    name: str
    description: str | None
    created_at: datetime
    users_count: int
    permissions_count: int


class RoleCreate(BaseModel):
    name: str
    description: str | None = None


class RoleUpdate(BaseModel):
    name: str
    description: str | None = None
