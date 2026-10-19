from datetime import date

from pydantic import BaseModel, ConfigDict


class Base(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class DivisionRead(Base):
    id: int
    name: str


class DivisionDetails(DivisionRead):
    group_count: int


class DivisionCreate(Base):
    name: str


class DivisionUpdate(Base):
    name: str


class GroupTypeRead(Base):
    id: int
    name: str


class GroupTypeDetails(GroupTypeRead):
    group_count: int


class GroupRead(Base):
    id: int
    name: str
    division: DivisionRead
    group_type: GroupTypeRead


class GroupOverview(Base):
    id: int
    name: str
    division_id: int
    division_name: str
    group_type_id: int
    group_type_name: str
    rules_count: int
    repartitions_count: int


class GroupCreate(Base):
    name: str
    division_id: int
    group_type_id: int


class GroupUpdate(Base):
    name: str
    division_id: int
    group_type_id: int


class GroupLookup(Base):
    id: int
    description: str


class RuleRead(Base):
    id: int
    name: str
    valid_from: date
    valid_to: date | None
    percent_value: float


class RuleCreate(Base):
    name: str
    valid_from: date
    valid_to: date | None = None
    percent_value: float


class RuleUpdate(Base):
    name: str
    valid_from: date
    valid_to: date | None = None
    percent_value: float


class TargetRead(Base):
    id: int
    group_id: int
    group_name: str
    allocation_type: str
    percent_value: float | None


class TargetCreate(Base):
    group_id: int
    allocation_type: str
    percent_value: float | None


class TargetUpdate(Base):
    group_id: int
    allocation_type: str
    percent_value: float | None


class DepartmentRepartitionRead(Base):
    id: int
    department_id: int
    department_name: str
    valid_from: date
    valid_to: date | None
    is_active: bool


class DepartmentRepartitionCreate(Base):
    department_id: int
    valid_from: date
    valid_to: date | None = None


class DepartmentRepartitionUpdate(Base):
    department_id: int
    valid_from: date
    valid_to: date | None = None


class DepartmentRead(Base):
    id: int
    code: str
    name: str
    brand: str
