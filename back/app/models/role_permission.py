from pydantic import BaseModel


class RolePermission(BaseModel):
    role_id: int
    permission_id: int
