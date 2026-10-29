from pydantic import BaseModel, ConfigDict, Field, computed_field


class PaginationParams(BaseModel):
    model_config = ConfigDict(extra="forbid")
    page: int = Field(1, ge=1)
    limit: int = Field(10, ge=1, le=100)

    @computed_field
    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit
