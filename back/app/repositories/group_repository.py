from app.domains.finance import (
    Group,
    GroupOverview,
)
from app.filters.finance import GroupFilter
from app.repositories.base import BaseRepository, LookupObjects, LookupResponse


class GroupRepository(BaseRepository):
    def lookup(self, search: str) -> list[LookupResponse]:
        return self._lookup(LookupObjects.GROUPS, search)

    def get_by_id(self, id) -> GroupOverview | None:
        sql = """
            SELECT
                g.id,
                g.name,
                division_id = d.id,
                division_name = d.name,
                group_type_id = gt.id,
                group_type_name = gt.name,
                rules_count = (SELECT COUNT(*) FROM finance.factGroupRules AS r
                                WHERE r.group_id = g.id),
                repartitions_count = (SELECT COUNT(*) FROM finance.factDepartmentsRepartition AS r
                                    WHERE r.group_id = g.id)

            FROM finance.dimGroups AS g
            LEFT JOIN finance.dimDivision   AS d  ON d.id  = g.division_id
            LEFT JOIN finance.dimGroupTypes AS gt ON gt.id = g.group_type_id
            where g.id = :id
        """
        rows = self._fetch_one_or_none(sql, {"id": id})

        return GroupOverview.model_validate(rows) if rows else None

    def get_by_id_light(self, id) -> Group | None:
        sql = """
            select
                *
            from finance.dimGroups
            where id = :id
        """
        row = self._fetch_one_or_none(sql, {"id": id})

        return Group.model_validate(row) if row else None

    def get_by_name(self, name) -> Group | None:
        sql = """
            select
                *
            from finance.dimGroups
            where name = :name
        """
        row = self._fetch_one_or_none(sql, {"name": name})

        return Group.model_validate(row) if row else None

    def get_all(self, filters: GroupFilter) -> tuple[list[GroupOverview], int]:
        conditions = []

        if filters.division_ids:
            conditions.append("g.division_id IN :division_ids")

        if filters.group_type_ids:
            conditions.append("g.group_type_id IN :group_type_ids")

        if filters.search:
            conditions.append("g.name LIKE :search_pattern")

        sql = """
        select
            g.id,
            g.name,
            division_id = d.id,
            division_name = d.name,
            group_type_id = gt.id,
            group_type_name = gt.name,
            rules_count = (SELECT COUNT(*) FROM finance.factGroupRules AS r
                            WHERE r.group_id = g.id),
            repartitions_count = (SELECT COUNT(*) FROM finance.factDepartmentsRepartition AS r
                                WHERE r.group_id = g.id)
        from finance.dimGroups AS g
        LEFT JOIN finance.dimDivision AS d ON d.id = g.division_id
        LEFT JOIN finance.dimGroupTypes AS gt ON gt.id = g.group_type_id
"""
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)

        sql += """
            ORDER BY g.id
            OFFSET :offset ROWS
            FETCH NEXT :limit ROWS ONLY
        """

        rows = self._fetch_all(sql, filters.model_dump())

        sql_total = "SELECT COUNT(*) FROM finance.dimGroups g"
        if conditions:
            sql_total += " WHERE " + " AND ".join(conditions)

        total = self._scalar(sql_total, filters.model_dump())
        return [GroupOverview.model_validate(row) for row in rows], total

    def create(self, name: str, group_type_id: int, division_id: int) -> int:
        params = {
            "name": name,
            "group_type_id": group_type_id,
            "division_id": division_id,
        }
        sql = """
            insert into finance.dimGroups (name, division_id, group_type_id)
            OUTPUT inserted.id
            values (:name, :division_id, :group_type_id)
        """

        return self._scalar(sql, params)

    def update(self, id: int, name: str, division_id: int, group_type_id: int):
        sql = """
            update finance.dimGroups
            set name = :name,
                division_id = :division_id,
                group_type_id = :group_type_id
            where id = :id
        """
        self._execute(
            sql,
            {
                "id": id,
                "name": name,
                "division_id": division_id,
                "group_type_id": group_type_id,
            },
        )

    def delete(self, id: int) -> None:
        sql = """
            delete from finance.dimGroups
            where id = :id
        """
        self._execute(sql, {"id": id})

    def get_by_division_id_light(self, id: int) -> list[Group]:
        sql = """
            select
                *
            from finance.dimGroups
            where division_id = :id
        """
        rows = self._fetch_all(sql, {"id": id})
        return [Group.model_validate(row) for row in rows]
