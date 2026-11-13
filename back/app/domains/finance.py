from datetime import date

from app.domains.domain_model import DomainModel


class Division(DomainModel):
    id: int
    name: str
    is_administrative: bool
    company_id: int


class DivisionDetail(DomainModel):
    id: int
    name: str
    is_administrative: bool
    company_id: int
    company_name: str
    group_count: int


class GroupFilter(DomainModel):
    search: str | None = None
    division_ids: list[int] | None = None
    group_type_ids: list[int] | None = None
    limit: int = 50
    offset: int = 0


class GroupType(DomainModel):
    id: int
    name: str


class Group(DomainModel):
    id: int
    name: str
    division_id: int
    group_type_id: int
    parent_id: int | None = None
    parent_type_id: int | None = None


class GroupFolder(DomainModel):
    id: int
    name: str


class GroupDetail(DomainModel):
    id: int
    name: str
    division: Division
    group_type: GroupType


class GroupOverview(DomainModel):
    id: int
    name: str
    division_id: int
    division_name: str
    group_type_id: int
    group_type_name: str
    rules_count: int
    repartitions_count: int
    parent_id: int | None = None
    parent_name: str | None = None


class GroupLookup(DomainModel):
    id: int
    description: str


class GroupRule(DomainModel):
    id: int
    name: str
    group_id: int
    valid_from: date
    valid_to: date | None
    percent_value: float


class GroupRuleTarget(DomainModel):
    id: int
    group_id: int
    group_name: str
    allocation_type: str
    percent_value: float | None


class Deparment(DomainModel):
    id: int
    code: str
    name: str
    brand: str
