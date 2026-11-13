from datetime import date
from decimal import Decimal

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.db.models.finance import GroupRule


class GroupRuleRepo:
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, rule_id: int) -> GroupRule | None:
        return self._session.get(GroupRule, rule_id)

    def get_by_id_and_group_id(self, rule_id: int, group_id: int) -> GroupRule | None:
        stmt = select(GroupRule).where(
            GroupRule.id == rule_id,
            GroupRule.group_id == group_id,
        )
        return self._session.scalar(stmt)

    def get_by_group_id(self, group_id: int) -> list[GroupRule]:
        stmt = (
            select(GroupRule)
            .where(GroupRule.group_id == group_id)
            .order_by(GroupRule.valid_from.desc(), GroupRule.id)
        )
        return list(self._session.scalars(stmt))

    def create(
        self,
        group_id: int,
        name: str,
        valid_from: date,
        valid_to: date | None,
        percent_value: Decimal,
    ) -> int:
        rule = GroupRule(
            group_id=group_id,
            name=name,
            valid_from=valid_from,
            valid_to=valid_to,
            percent_value=percent_value,
        )
        self._session.add(rule)
        self._session.flush()
        return rule.id

    def delete(self, rule: GroupRule) -> None:
        self._session.delete(rule)

    def has_overlapping_rule(
        self,
        group_id: int,
        valid_from: date,
        valid_to: date | None,
        exclude_id: int | None = None,
    ) -> bool:
        stmt = select(GroupRule.id).where(
            GroupRule.group_id == group_id,
            or_(
                GroupRule.valid_to.is_(None),
                GroupRule.valid_to >= valid_from,
            ),
        )

        if valid_to is not None:
            stmt = stmt.where(GroupRule.valid_from <= valid_to)

        if exclude_id is not None:
            stmt = stmt.where(GroupRule.id != exclude_id)

        return self._session.scalar(stmt.limit(1)) is not None
