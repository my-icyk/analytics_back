from app.domains.finance import Division
from app.repositories.base import BaseRepository


class DivisionRepository(BaseRepository):
    def get_by_id(self, division_id) -> Division | None:

        sql = """
            SELECT
                d.id,
                d.name,
                group_count = count(g.id)
            FROM finance.dimDivision AS d
            LEFT JOIN finance.dimGroups AS g ON g.division_id = d.id
            WHERE
                d.id = :division_id
            GROUP BY
                d.id,
                d.name
            ORDER BY
                d.name,
                d.id
        """
        result = self._fetch_one_or_none(sql, {"division_id": division_id})
        return Division.model_validate(result) if result else None

    def get_by_name(self, name) -> Division | None:

        sql = """
            SELECT
                d.id,
                d.name,
                group_count = count(g.id)
            FROM finance.dimDivision AS d
            LEFT JOIN finance.dimGroups AS g ON g.division_id = d.id
            WHERE
                d.name = :name
            GROUP BY
                d.id,
                d.name
            ORDER BY
                d.name,
                d.id
        """
        result = self._fetch_one_or_none(sql, {"name": name})
        return Division.model_validate(result) if result else None

    def get_all(self) -> list[Division]:

        sql = """
            SELECT
                d.id,
                d.name,
                group_count = count(g.id)
            FROM finance.dimDivision AS d
            LEFT JOIN finance.dimGroups AS g ON g.division_id = d.id
            GROUP BY
                d.id,
                d.name
            ORDER BY
                d.name,
                d.id
        """
        results = self._fetch_all(sql)
        return [Division.model_validate(result) for result in results]

    def create(self, name: str) -> Division:

        sql = """
            INSERT INTO finance.dimDivision (name)
            OUTPUT INSERTED.*
            VALUES (:name)
        """
        result = self._fetch_one(sql, {"name": name})
        return Division.model_validate(result)

    def update(self, id, name) -> Division:
        sql = """
            UPDATE finance.dimDivision
            SET name = :name
            OUTPUT INSERTED.*
            WHERE id = :id
        """
        result = self._fetch_one(sql, {"id": id, "name": name})
        return Division.model_validate(result)

    def delete(self, id) -> None:

        sql = """
            DELETE FROM finance.dimDivision
            WHERE id = :id
        """
        self._execute(sql, {"id": id})
