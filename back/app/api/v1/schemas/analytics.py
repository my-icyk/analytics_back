from pydantic import Field

from app.api.v1.schemas.finance import Base


class ProcedureCreate(Base):
    name: str
    exec_order: int


class ProcedureUpdate(Base):
    name: str = Field(min_length=1, max_length=200)
    exec_order: int = Field(ge=0)
    is_active: bool
