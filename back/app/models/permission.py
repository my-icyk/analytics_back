from pydantic import BaseModel


class Permission(BaseModel):
    id: int
    name: str
