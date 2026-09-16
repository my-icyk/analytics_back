from datetime import date

from app.domains.finance import GroupRule
from app.repositories.base import BaseRepository


class GroupRuleRepository(BaseRepository):
    def get_by_id(self, id: int) -> GroupRule | None:
        sql = """
            select *
            from finance.factGroupRules
            where id = :id
        """
        row = self._fetch_one_or_none(sql, {"id": id})
        return GroupRule.model_validate(row) if row else None

    def get_by_group_id(self, group_id: int) -> list[GroupRule]:
        sql = """
            select *
            from finance.factGroupRules
            where group_id = :group_id
        """
        rows = self._fetch_all(sql, {"group_id": group_id})
        return [GroupRule.model_validate(row) for row in rows]

    def create(
        self,
        name: str,
        group_id: int,
        valid_from: date,
        valid_to: date | None,
        percent_value: float,
    ) -> GroupRule:
        sql = """
            insert into finance.factGroupRules (name, group_id, valid_from, valid_to, percent_value)
            OUTPUT inserted.*
            values (:name, :group_id, :valid_from, :valid_to, :percent_value)
        """
        row = self._fetch_one(
            sql,
            {
                "name": name,
                "group_id": group_id,
                "valid_from": valid_from,
                "valid_to": valid_to,
                "percent_value": percent_value,
            },
        )
        return GroupRule.model_validate(row)

    def update(
        self,
        id: int,
        name: str,
        group_id: int,
        valid_from: date,
        valid_to: date | None,
        percent_value: float,
    ) -> GroupRule:
        sql = """
            update finance.factGroupRules
            set name = :name,
                group_id = :group_id,
                valid_from = :valid_from,
                valid_to = :valid_to,
                percent_value = :percent_value
            OUTPUT inserted.*
            where id = :id

        """
        row = self._fetch_one(
            sql,
            {
                "id": id,
                "name": name,
                "group_id": group_id,
                "valid_from": valid_from,
                "valid_to": valid_to,
                "percent_value": percent_value,
            },
        )
        return GroupRule.model_validate(row)

    def delete(self, id: int) -> None:
        sql = """
            delete from finance.factGroupRules
            where id = :id
        """
        self._execute(sql, {"id": id})

    def has_overlapping_rule(
        self,
        group_id: int,
        valid_from: date,
        valid_to: date | None,
        exclude_id: int = 0,
    ) -> bool:
        sql = """
            select 1
            from finance.factGroupRules
            where group_id = :group_id
            and id != :exclude_id
            and valid_from <= ISNULL(:valid_to, '9999-12-31')
            and valid_to >= :valid_from
        """
        row = self._fetch_one_or_none(
            sql,
            {
                "group_id": group_id,
                "valid_from": valid_from,
                "valid_to": valid_to,
                "exclude_id": exclude_id,
            },
        )
        return row is not None
