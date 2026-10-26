from pydantic import BaseModel, Field


class SetRolePermissionsRequest(BaseModel):
    permission_ids: list[int] = Field(default_factory=list)
