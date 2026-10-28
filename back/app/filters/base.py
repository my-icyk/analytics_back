from pydantic import BaseModel, Field


class PaginationFilter(BaseModel):
    limit: int = Field(default=50, ge=1)
    offset: int = Field(default=0, ge=0)
