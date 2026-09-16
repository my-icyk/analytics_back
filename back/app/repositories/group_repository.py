from app.domains.finance import Group, GroupDetail
from app.repositories.base import BaseRepository


class GroupRepository(BaseRepository):
    def _map_group_detail(self, row) -> GroupDetail:
        division = {
            "id": row["division_id"],
            "name": row["division_name"],
        }
        group_type = {
            "id": row["group_type_id"],
            "name": row["group_type_name"],
        }

        return GroupDetail.model_validate(
            {
                "id": row["group_id"],
                "name": row["group_name"],
                "division": division,
                "group_type": group_type,
            }
        )

    def get_by_id(self, id) -> GroupDetail | None:
        sql = """
            select
                group_id = g.id,
                group_name = g.name,
                division_id = d.id,
                division_name = d.name,
                group_type_id = gt.id,
                group_type_name = gt.name
            from finance.dimGroups AS g
            LEFT JOIN finance.dimDivision AS d ON d.id = g.division_id
            LEFT JOIN finance.dimGroupTypes AS gt ON gt.id = g.group_type_id
            where g.id = :id
        """
        rows = self._fetch_one_or_none(sql, {"id": id})

        return self._map_group_detail(rows) if rows else None

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

    def get_all(self) -> list[GroupDetail]:
        sql = """
            select
                group_id = g.id,
                group_name = g.name,
                division_id = d.id,
                division_name = d.name,
                group_type_id = gt.id,
                group_type_name = gt.name
            from finance.dimGroups AS g
            LEFT JOIN finance.dimDivision AS d ON d.id = g.division_id
            LEFT JOIN finance.dimGroupTypes AS gt ON gt.id = g.group_type_id
        """
        rows = self._fetch_all(sql)

        return [self._map_group_detail(row) for row in rows]

    def create(self, name: str, group_type_id: int, division_id: int) -> Group:
        sql = """
            insert into finance.dimGroups (name, division_id, group_type_id)
            OUTPUT inserted.*
            values (:name, :division_id, :group_type_id)
        """
        row = self._fetch_one(
            sql,
            {"name": name, "group_type_id": group_type_id, "division_id": division_id},
        )
        return Group.model_validate(row)

    def update(self, id: int, name: str, division_id: int, group_type_id: int) -> Group:
        sql = """
            update finance.dimGroups
            set name = :name,
                division_id = :division_id,
                group_type_id = :group_type_id
            OUTPUT inserted.*
            where id = :id
        """
        row = self._fetch_one(
            sql,
            {
                "id": id,
                "name": name,
                "division_id": division_id,
                "group_type_id": group_type_id,
            },
        )
        return Group.model_validate(row)

    def delete(self, id: int) -> None:
        sql = """
            delete from finance.dimGroups
            where id = :id
        """
        self._execute(sql, {"id": id})

    def get_by_division_id(self, division_id: int) -> list[GroupDetail]:
        sql = """
            select
                group_id = g.id,
                group_name = g.name,
                division_id = d.id,
                division_name = d.name,
                group_type_id = gt.id,
                group_type_name = gt.name
            from finance.dimGroups AS g
            LEFT JOIN finance.dimDivision AS d ON d.id = g.division_id
            LEFT JOIN finance.dimGroupTypes AS gt ON gt.id = g.group_type_id
            where g.division_id = :division_id
        """
        rows = self._fetch_all(sql, {"division_id": division_id})
        return [self._map_group_detail(row) for row in rows]

    def get_by_division_id_light(self, id: int) -> list[Group]:
        sql = """
            select
                *
            from finance.dimGroups
            where division_id = :id
        """
        rows = self._fetch_all(sql, {"id": id})
        return [Group.model_validate(row) for row in rows]
