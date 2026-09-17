from datetime import date

from app.domains.domain_model import DomainModel


class Division(DomainModel):
    id: int
    name: str


class GroupFilter(DomainModel):
    group_ids: list[int] | None = None
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


class GroupDetail(DomainModel):
    id: int
    name: str
    division: Division
    group_type: GroupType


class GroupPage(DomainModel):
    items: list[GroupDetail]
    total: int


class GroupRule(DomainModel):
    id: int
    name: str
    group_id: int
    valid_from: date
    valid_to: date | None
    percent_value: float


class GroupRuleTarget(DomainModel):
    id: int
    rule_id: int
    group_id: int
    allocation_type: str
    percent_value: float | None
