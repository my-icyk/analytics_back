from pydantic import BaseModel


class RoleRead(BaseModel):
    id: int
    name: str
    description: str | None


class RoleCreate(BaseModel):
    name: str
    description: str | None


class RoleUpdate(BaseModel):
    name: str
    description: str | None
