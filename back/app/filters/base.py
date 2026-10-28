from pydantic import BaseModel, ConfigDict, Field


class PaginationFilter(BaseModel):
    model_config = ConfigDict(extra="forbid")
    limit: int = Field(default=50, ge=1)
    offset: int = Field(default=0, ge=0)
