from datetime import date

from app.domains.finance import GroupRule, GroupRuleTarget
from app.exceptions.exceptions import (
    NotFoundError,
    OverlappingPeriodError,
)
from app.repositories.group_repository import GroupRepository
from app.repositories.group_rule_repository import GroupRuleRepository
from app.repositories.group_rule_target_repository import GroupRuleTargetRepository


class FinanceRuleService:
    def __init__(
        self,
        group_repository: GroupRepository,
        group_rule_repository: GroupRuleRepository,
        group_rule_target_repository: GroupRuleTargetRepository,
    ):
        self.group_repository = group_repository
        self.group_rule_repository = group_rule_repository
        self.group_rule_target_repository = group_rule_target_repository

    def _validate_group_exists(self, group_id: int):
        if not self.group_repository.get_by_id_light(group_id):
            raise NotFoundError("Group", "id", str(group_id))

    def _validate_overlapping_rule(
        self,
        group_id: int,
        valid_from: date,
        valid_to: date | None,
        exclude_id: int = 0,
    ):
        if self.group_rule_repository.has_overlapping_rule(
            group_id=group_id,
            valid_from=valid_from,
            valid_to=valid_to,
            exclude_id=exclude_id,
        ):
            raise OverlappingPeriodError(
                entity_name="GroupRule",
                valid_from=valid_from,
                valid_to=valid_to,
            )

    # TODO: Check if all targets are 100% with one proportional minim
    def get_rule(self, id: int) -> GroupRule:
        group_rule = self.group_rule_repository.get_by_id(id)
        if not group_rule:
            raise NotFoundError("GroupRule", "id", str(id))

        return group_rule

    def get_rules_by_group_id(self, group_id: int) -> list[GroupRule]:
        self._validate_group_exists(group_id)
        return self.group_rule_repository.get_by_group_id(group_id)

    def create_rule(
        self,
        name: str,
        group_id: int,
        valid_from: date,
        valid_to: date | None,
        percent_value: float,
    ) -> GroupRule:
        self._validate_group_exists(group_id)
        self._validate_overlapping_rule(
            group_id=group_id,
            valid_from=valid_from,
            valid_to=valid_to,
            exclude_id=0,
        )

        return self.group_rule_repository.create(
            name=name,
            group_id=group_id,
            valid_from=valid_from,
            valid_to=valid_to,
            percent_value=percent_value,
        )

    def update_rule(
        self,
        id: int,
        name: str,
        group_id: int,
        valid_from: date,
        valid_to: date | None,
        percent_value: float,
    ) -> GroupRule:
        self.get_rule(id)
        self._validate_group_exists(group_id)
        self._validate_overlapping_rule(
            group_id=group_id,
            valid_from=valid_from,
            valid_to=valid_to,
            exclude_id=id,
        )

        # proceed to update the rule
        return self.group_rule_repository.update(
            id=id,
            name=name,
            group_id=group_id,
            valid_from=valid_from,
            valid_to=valid_to,
            percent_value=percent_value,
        )

    def delete_rule(self, id: int) -> None:
        self.get_rule(id)
        self.group_rule_target_repository.delete_by_rule_id(id)
        self.group_rule_repository.delete(id)

    def get_target(self, id: int) -> GroupRuleTarget:
        target = self.group_rule_target_repository.get_by_id(id)
        if not target:
            raise NotFoundError("GroupRuleTarget", "id", str(id))

        return target

    def get_targets(self, rule_id: int) -> list[GroupRuleTarget]:
        self.get_rule(rule_id)
        targets = self.group_rule_target_repository.get_by_rule_id(rule_id)

        return targets

    def assign_target(
        self,
        rule_id: int,
        group_id: int,
        allocation_type: str,
        percent_value: float | None,
    ) -> GroupRuleTarget:
        self.get_rule(rule_id)

        return self.group_rule_target_repository.create(
            rule_id=rule_id,
            group_id=group_id,
            allocation_type=allocation_type,
            percent_value=percent_value,
        )

    def update_target(
        self,
        id: int,
        rule_id: int,
        group_id: int,
        allocation_type: str,
        percent_value: float | None,
    ) -> GroupRuleTarget:
        self.get_rule(rule_id)
        return self.group_rule_target_repository.update(
            id=id,
            rule_id=rule_id,
            group_id=group_id,
            allocation_type=allocation_type,
            percent_value=percent_value,
        )

    def remove_target(self, target_id: int, rule_id: int) -> None:
        target = self.group_rule_target_repository.get_by_id_and_rule_id(
            target_id, rule_id
        )
        if not target:
            raise NotFoundError("GroupRuleTarget", "id", str(target_id))
        self.group_rule_target_repository.delete(target_id)
