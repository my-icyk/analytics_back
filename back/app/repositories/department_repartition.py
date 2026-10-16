from datetime import date

from app.domains.finance import Deparment, DepartmentRepartition
from app.repositories.base import BaseRepository, LookupObjects, LookupResponse


class DepartmentRepartitionRepository(BaseRepository):
    # TODO: De refacut codul acesta
    def get_by_id(self, id: int) -> DepartmentRepartition:
        sql = """
            select 
                main.id,
                main.department_id,
                department_code = d.code,
                department_name = d.name,
                main.group_id,
                main.valid_from,
                main.valid_to
            from finance.factDepartmentsRepartition AS main
            JOIN finance.dimDepartments d ON d.id = main.department_id
            where main.id = :id
        """
        row = self._fetch_one(sql, {"id": id})
        return DepartmentRepartition.model_validate(row)

    def get_by_group_id(self, group_id: int) -> list[DepartmentRepartition]:
        sql = """
            declare @date date = GETDATE()
            select 
                main.id,
                department = CONCAT(d.name, ' (', d.id, ')'),
                is_active = op.is_active,
                main.valid_from,
                main.valid_to
            from finance.factDepartmentsRepartition AS main
            JOIN finance.dimDepartments d ON d.id = main.department_id
            outer apply (
                SELECT
                is_active = IIF(@date BETWEEN main.valid_from AND ISNULL(main.valid_to, '9999-12-31'), 1, 0)
            ) as op
            where main.group_id = :group_id
            ORDER BY 
                op.is_active DESC,
                main.valid_to ASC
        """
        rows = self._fetch_all(sql, {"group_id": group_id})
        return [DepartmentRepartition.model_validate(row) for row in rows]

    def create(
        self,
        department_id: int,
        group_id: int,
        valid_from: date,
        valid_to: date | None,
    ) -> DepartmentRepartition:
        sql = """
            insert into finance.factDepartmentsRepartition (department_id, group_id, valid_from, valid_to)
            OUTPUT inserted.id
            values (:department_id, :group_id, :valid_from, :valid_to)
        """
        id = self._scalar(
            sql,
            {
                "department_id": department_id,
                "group_id": group_id,
                "valid_from": valid_from,
                "valid_to": valid_to,
            },
        )
        row = self.get_by_id(id)
        return DepartmentRepartition.model_validate(row)

    def update(
        self,
        id: int,
        department_id: int,
        group_id: int,
        valid_from: date,
        valid_to: date | None,
    ) -> None:
        sql = """
            update finance.factDepartmentsRepartition
            set department_id = :department_id,
                group_id = :group_id,
                valid_from = :valid_from,
                valid_to = :valid_to
            
            where id = :id
        """
        self._execute(
            sql,
            {
                "id": id,
                "department_id": department_id,
                "group_id": group_id,
                "valid_from": valid_from,
                "valid_to": valid_to,
            },
        )

    def delete(self, id: int, group_id: int) -> None:
        sql = """
            delete from finance.factDepartmentsRepartition
            where id = :id and group_id = :group_id
        """
        self._execute(sql, {"id": id, "group_id": group_id})

    def get_departments(self) -> list[Deparment]:
        sql = """
            select
                id,
                code,
                name,
                brand
            from finance.dimDepartments
            order by
                brand ASC,
                name ASC
        """
        rows = self._fetch_all(sql)
        return [Deparment.model_validate(row) for row in rows]

    def lookup(self, search: str) -> list[LookupResponse]:
        return self._lookup(LookupObjects.DEPARTMENTS, search)
