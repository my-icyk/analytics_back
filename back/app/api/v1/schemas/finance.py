from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class Base(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class DivisionRead(Base):
    id: int
    name: str
    is_administrative: bool
    company_id: int
    company_name: str


class DivisionDetails(DivisionRead):
    group_count: int


class DivisionCreate(Base):
    name: str
    is_administrative: bool
    company_id: int


class DivisionUpdate(DivisionCreate): ...


class GroupTypeRead(Base):
    id: int
    name: str


class GroupTypeDetails(GroupTypeRead):
    group_count: int


class GroupRead(Base):
    id: int
    name: str
    division_id: int
    division_name: str
    group_type_id: int
    group_type_name: str
    rules_count: int
    repartitions_count: int
    parent_id: int | None
    parent_name: str | None


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
    parent_id: int | None = None


class GroupUpdate(Base):
    name: str
    division_id: int
    group_type_id: int
    parent_id: int | None = None


class GroupLookup(Base):
    id: int
    description: str


class RuleRead(Base):
    id: int
    name: str
    valid_from: date
    valid_to: date | None
    percent_value: Decimal


class RuleCreate(Base):
    name: str
    valid_from: date
    valid_to: date | None = None
    percent_value: Decimal = Field(ge=0, le=100)


class RuleUpdate(Base):
    name: str
    valid_from: date
    valid_to: date | None = None
    percent_value: Decimal = Field(ge=0, le=100)


class TargetRead(Base):
    id: int
    group_id: int
    group_name: str
    allocation_type: str
    percent_value: Decimal | None


class TargetCreate(Base):
    group_id: int
    allocation_type: str
    percent_value: Decimal | None


class TargetUpdate(Base):
    group_id: int
    allocation_type: str
    percent_value: Decimal | None


class DepartmentRepartitionRead(Base):
    id: int
    department_id: int
    department_code: str
    department_name: str
    valid_from: date
    valid_to: date | None
    is_active: bool
    brand_name: str


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


class CopyTargetsIn(Base):
    source_rule_id: int


class CompanyRead(Base):
    id: int
    name: str
