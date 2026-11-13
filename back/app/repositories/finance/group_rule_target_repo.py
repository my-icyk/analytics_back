from decimal import Decimal

from sqlalchemy import delete, insert, literal, select
from sqlalchemy.orm import Session

from app.db.models.finance import GroupRuleTarget


class GroupRuleTargetRepo:
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> GroupRuleTarget | None:
        return self._session.get(GroupRuleTarget, id)

    def get_by_id_and_rule_id(self, id: int, rule_id: int) -> GroupRuleTarget | None:
        stmt = select(GroupRuleTarget).where(
            GroupRuleTarget.id == id,
            GroupRuleTarget.rule_id == rule_id,
        )
        return self._session.scalar(stmt)

    def get_by_rule_id(self, rule_id: int) -> list[GroupRuleTarget]:
        stmt = (
            select(GroupRuleTarget)
            .where(GroupRuleTarget.rule_id == rule_id)
            .order_by(GroupRuleTarget.id)
        )
        return list(self._session.scalars(stmt))

    def create(
        self,
        rule_id: int,
        group_id: int,
        allocation_type: str,
        percent_value: Decimal | None,
    ) -> int:
        target = GroupRuleTarget(
            rule_id=rule_id,
            group_id=group_id,
            allocation_type=allocation_type,
            percent_value=percent_value,
        )
        self._session.add(target)
        self._session.flush()
        return target.id

    def delete(self, target: GroupRuleTarget) -> None:
        self._session.delete(target)

    def delete_by_rule_id(self, rule_id: int) -> None:
        stmt = delete(GroupRuleTarget).where(GroupRuleTarget.rule_id == rule_id)
        self._session.execute(stmt)

    def create_from_rule(self, rule_id: int, source_rule_id: int) -> None:
        source_targets = select(
            literal(rule_id),
            GroupRuleTarget.group_id,
            GroupRuleTarget.allocation_type,
            GroupRuleTarget.percent_value,
        ).where(GroupRuleTarget.rule_id == source_rule_id)

        stmt = insert(GroupRuleTarget).from_select(
            ["rule_id", "group_id", "allocation_type", "percent_value"],
            source_targets,
        )
        self._session.execute(stmt)
