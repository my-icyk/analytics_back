from datetime import date

from pydantic import BaseModel, ConfigDict


class Base(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class DivisionRead(Base):
    id: int
    name: str


class DivisionCreate(Base):
    name: str


class DivisionUpdate(Base):
    name: str


class GroupTypeRead(Base):
    id: int
    name: str


class GroupRead(Base):
    id: int
    name: str
    division: DivisionRead
    group_type: GroupTypeRead


class GroupCreate(Base):
    name: str
    division_id: int
    group_type_id: int


class GroupUpdate(Base):
    name: str
    division_id: int
    group_type_id: int


class RuleRead(Base):
    id: int
    name: str
    group_id: int
    valid_from: date
    valid_to: date | None
    percent_value: float


class RuleCreate(Base):
    name: str
    group_id: int
    valid_from: date
    valid_to: date | None
    percent_value: float


class RuleUpdate(Base):
    name: str
    group_id: int
    valid_from: date
    valid_to: date | None
    percent_value: float


class TargetRead(Base):
    id: int
    rule_id: int
    group_id: int
    allocation_type: str
    percent_value: float | None


class TargetCreate(Base):
    rule_id: int
    group_id: int
    allocation_type: str
    percent_value: float | None


class TargetUpdate(Base):
    rule_id: int
    group_id: int
    allocation_type: str
    percent_value: float | None
