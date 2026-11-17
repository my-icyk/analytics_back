from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session

from app.db.models.finance import GroupRule, GroupRuleTarget
from app.exceptions.exceptions import (
    BadRequestError,
    NotFoundError,
    OverlappingPeriodError,
)
from app.repositories.finance import (
    GroupRuleRepo,
    GroupRuleTargetRepo,
)
from app.repositories.finance.group_repo import GroupRepo
from app.services.common import WriteService


class FinanceRuleService(WriteService):
    def __init__(
        self,
        session: Session,
        *,
        group_repo: GroupRepo,
        group_rule_repo: GroupRuleRepo,
        group_rule_target_repo: GroupRuleTargetRepo,
    ) -> None:
        super().__init__(session)
        self._groups = group_repo
        self._rules = group_rule_repo
        self._targets = group_rule_target_repo

    def _validate_group_exists(self, group_id: int) -> None:
        if self._groups.get_by_id_light(group_id) is None:
            raise NotFoundError("Group", "id", str(group_id))

    def _get_rule_for_group(self, group_id: int, rule_id: int) -> GroupRule:
        rule = self._rules.get_by_id_and_group_id(
            rule_id=rule_id,
            group_id=group_id,
        )
        if rule is None:
            raise NotFoundError("GroupRule", "id", str(rule_id))
        return rule

    def _get_target_for_rule(self, rule_id: int, target_id: int) -> GroupRuleTarget:
        target = self._targets.get_by_id_and_rule_id(id=target_id, rule_id=rule_id)
        if target is None:
            raise NotFoundError("GroupRuleTarget", "id", str(target_id))
        return target

    def get_rule(self, id: int) -> GroupRule:
        rule = self._rules.get_by_id(id)
        if rule is None:
            raise NotFoundError("GroupRule", "id", str(id))
        return rule

    def get_rules_by_group_id(self, group_id: int) -> list[GroupRule]:
        self._validate_group_exists(group_id)
        return self._rules.get_by_group_id(group_id)

    def create_rule(
        self,
        group_id: int,
        name: str,
        valid_from: date,
        valid_to: date | None,
        percent_value: Decimal,
    ) -> int:
        with self._write():
            self._validate_group_exists(group_id)
            rule_id = self._rules.create(
                group_id=group_id,
                name=name,
                valid_from=valid_from,
                valid_to=valid_to,
                percent_value=percent_value,
            )
        return rule_id

    def update_rule(
        self,
        group_id: int,
        rule_id: int,
        name: str,
        valid_from: date,
        valid_to: date | None,
        percent_value: Decimal,
    ) -> None:
        with self._write():
            rule = self._get_rule_for_group(group_id, rule_id)

            if self._rules.has_overlapping_rule(
                group_id=group_id,
                valid_from=valid_from,
                valid_to=valid_to,
                exclude_id=rule.id,
            ):
                raise OverlappingPeriodError(
                    entity_name="GroupRule",
                    valid_from=valid_from,
                    valid_to=valid_to,
                )

            rule.name = name
            rule.valid_from = valid_from
            rule.valid_to = valid_to
            rule.percent_value = percent_value

    def delete_rule(self, group_id: int, rule_id: int) -> None:
        with self._write():
            rule = self._get_rule_for_group(group_id, rule_id)
            self._targets.delete_by_rule_id(rule.id)
            self._rules.delete(rule)

    def get_target(self, id: int) -> GroupRuleTarget:
        target = self._targets.get_by_id(id)
        if target is None:
            raise NotFoundError("GroupRuleTarget", "id", str(id))
        return target

    def get_targets(self, rule_id: int) -> list[GroupRuleTarget]:
        self.get_rule(rule_id)
        return self._targets.get_by_rule_id(rule_id)

    def assign_target(
        self,
        rule_id: int,
        group_id: int,
        allocation_type: str,
        percent_value: Decimal | None,
    ) -> int:
        with self._write():
            self.get_rule(rule_id)
            self._validate_group_exists(group_id)

            target_id = self._targets.create(
                rule_id=rule_id,
                group_id=group_id,
                allocation_type=allocation_type,
                percent_value=percent_value,
            )
        return target_id

    def update_target(
        self,
        id: int,
        rule_id: int,
        group_id: int,
        allocation_type: str,
        percent_value: Decimal | None,
    ) -> None:
        with self._write():
            target = self._get_target_for_rule(rule_id, id)
            self._validate_group_exists(group_id)

            target.group_id = group_id
            target.allocation_type = allocation_type
            target.percent_value = percent_value

    def remove_target(self, rule_id: int, target_id: int) -> None:
        with self._write():
            target = self._get_target_for_rule(rule_id, target_id)
            self._targets.delete(target)

    def replace_targets_from_rule(self, rule_id: int, source_rule_id: int) -> None:
        if rule_id == source_rule_id:
            raise BadRequestError("Cannot replace targets from the same rule.")

        with self._write():
            self.get_rule(rule_id)
            self.get_rule(source_rule_id)

            self._targets.delete_by_rule_id(rule_id)
            self._targets.create_from_rule(
                rule_id=rule_id,
                source_rule_id=source_rule_id,
            )
