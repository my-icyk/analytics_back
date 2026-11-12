from pydantic import BaseModel, Field, StrictBool


class AssignRolePermissionsRequest(BaseModel):
    permission_ids: list[int] = Field(default_factory=list)


class AssignUserRolesRequest(BaseModel):
    role_ids: list[int] = Field(default_factory=list)


class UserAdminUpdate(BaseModel):
    is_admin: StrictBool
