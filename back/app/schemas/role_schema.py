from datetime import datetime

from pydantic import BaseModel


class RoleRead(BaseModel):
    id: int
    name: str
    description: str | None
    created_at: datetime


class RoleCreate(BaseModel):
    name: str
    description: str | None
