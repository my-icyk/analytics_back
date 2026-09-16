from app.domains.finance import GroupRuleTarget
from app.repositories.base import BaseRepository


class GroupRuleTargetRepository(BaseRepository):
    def get_by_id(self, id: int) -> GroupRuleTarget | None:
        sql = """
            select *
            from finance.factGroupRulesTargets
            where id = :id
        """
        row = self._fetch_one_or_none(sql, {"id": id})
        return GroupRuleTarget.model_validate(row) if row else None

    def get_by_id_and_rule_id(self, id: int, rule_id: int) -> GroupRuleTarget | None:
        sql = """
            select *
            from finance.factGroupRulesTargets
            where
                id = :id and
                rule_id = :rule_id
        """
        row = self._fetch_one_or_none(sql, {"id": id, "rule_id": rule_id})
        return GroupRuleTarget.model_validate(row) if row else None

    def get_by_rule_id(self, rule_id: int) -> list[GroupRuleTarget]:
        sql = """
            select *
            from finance.factGroupRulesTargets
            where rule_id = :rule_id
        """
        rows = self._fetch_all(sql, {"rule_id": rule_id})
        return [GroupRuleTarget.model_validate(row) for row in rows]

    def create(
        self,
        rule_id: int,
        group_id: int,
        allocation_type: str,
        percent_value: float | None,
    ) -> GroupRuleTarget:
        sql = """
            insert into finance.factGroupRulesTargets (rule_id, group_id, allocation_type, percent_value)
            OUTPUT INSERTED.*
            values (:rule_id, :group_id, :allocation_type, :percent_value)

        """
        row = self._fetch_one(
            sql,
            {
                "rule_id": rule_id,
                "group_id": group_id,
                "allocation_type": allocation_type,
                "percent_value": percent_value,
            },
        )
        return GroupRuleTarget.model_validate(row)

    def update(
        self,
        id: int,
        rule_id: int,
        group_id: int,
        allocation_type: str,
        percent_value: float | None,
    ) -> GroupRuleTarget:
        sql = """
            update finance.factGroupRulesTargets
            set rule_id = :rule_id,
                group_id = :group_id,
                allocation_type = :allocation_type,
                percent_value = :percent_value
            OUTPUT INSERTED.*
            where id = :id
        """
        row = self._fetch_one(
            sql,
            {
                "id": id,
                "rule_id": rule_id,
                "group_id": group_id,
                "allocation_type": allocation_type,
                "percent_value": percent_value,
            },
        )
        return GroupRuleTarget.model_validate(row)

    def delete(self, id: int) -> None:
        sql = """
            delete from finance.factGroupRulesTargets
            where id = :id
        """
        self._execute(sql, {"id": id})

    def delete_by_rule_id(self, rule_id: int) -> None:
        sql = """
            delete from finance.factGroupRulesTargets
            where rule_id = :rule_id
        """
        self._execute(sql, {"rule_id": rule_id})
