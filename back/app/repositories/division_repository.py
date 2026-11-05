from app.domains.finance import DivisionDetail
from app.repositories.base import BaseRepository


class DivisionRepository(BaseRepository):
    def get_by_id(self, division_id) -> DivisionDetail | None:

        sql = """
            SELECT
                d.id,
                d.name,
                d.is_administrative,
                d.company_id,
                c.name AS company_name,
                group_count = count(g.id)
            FROM finance.dimDivision AS d
            LEFT JOIN finance.dimGroups AS g ON g.division_id = d.id
            LEFT JOIN finance.dimCompanies AS c ON c.id = d.company_id
            WHERE
                d.id = :division_id
            GROUP BY
                d.id,
                d.name,
                d.is_administrative,
                d.company_id,
                c.name
            ORDER BY
                d.name,
                d.id
        """
        result = self._fetch_one_or_none(sql, {"division_id": division_id})
        return DivisionDetail.model_validate(result) if result else None

    def get_by_name(self, name) -> DivisionDetail | None:

        sql = """
            SELECT
                d.id,
                d.name,
                d.is_administrative,
                d.company_id,
                c.name AS company_name,
                group_count = count(g.id)
            FROM finance.dimDivision AS d
            LEFT JOIN finance.dimGroups AS g ON g.division_id = d.id
            LEFT JOIN finance.dimCompanies AS c ON c.id = d.company_id
            WHERE
                d.name = :name
            GROUP BY
                d.id,
                d.name,
                d.is_administrative,
                d.company_id,
                c.name
            ORDER BY
                d.name,
                d.id
        """
        result = self._fetch_one_or_none(sql, {"name": name})
        return DivisionDetail.model_validate(result) if result else None

    def get_all(self) -> list[DivisionDetail]:

        sql = """
            SELECT
                d.id,
                d.name,
                d.is_administrative,
                d.company_id,
                c.name AS company_name,
                group_count = count(g.id)
            FROM finance.dimDivision AS d
            LEFT JOIN finance.dimGroups AS g ON g.division_id = d.id
            LEFT JOIN finance.dimCompanies AS c ON c.id = d.company_id
            GROUP BY
                d.id,
                d.name,
                d.is_administrative,
                d.company_id,
                c.name
            ORDER BY
                d.name,
                d.id
        """
        results = self._fetch_all(sql)
        return [DivisionDetail.model_validate(result) for result in results]

    def create(self, name: str, is_administrative: bool, company_id: int) -> int:

        sql = """
            INSERT INTO finance.dimDivision (name, is_administrative, company_id)
            OUTPUT INSERTED.id
            VALUES (:name, :is_administrative, :company_id)
        """
        id = self._scalar(
            sql,
            {
                "name": name,
                "is_administrative": is_administrative,
                "company_id": company_id,
            },
        )
        return id

    def update(
        self, id: int, name: str, is_administrative: bool, company_id: int
    ) -> None:
        sql = """
            UPDATE finance.dimDivision
            SET name = :name,
                is_administrative = :is_administrative,
                company_id = :company_id
              WHERE id = :id
        """
        self._execute(
            sql,
            {
                "id": id,
                "name": name,
                "is_administrative": is_administrative,
                "company_id": company_id,
            },
        )

    def delete(self, id: int) -> None:

        sql = """
            DELETE FROM finance.dimDivision
            WHERE id = :id
        """
        self._execute(sql, {"id": id})
