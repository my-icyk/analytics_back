from decimal import Decimal

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.db.models.hr.employee import Employee


class EmployeeRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, employee_id: int) -> Employee | None:
        return self._session.get(Employee, employee_id)

    def get_page(
        self,
        *,
        limit: int,
        offset: int,
        search: str | None = None,
    ) -> tuple[list[Employee], int]:
        predicates = []
        if search and search.strip():
            text = search.strip()
            predicates.append(
                or_(
                    *[
                        field.contains(text, autoescape=True)
                        for field in (
                            Employee.name,
                            Employee.employee_ref,
                            Employee.fiscal_code,
                            Employee.department_name,
                            Employee.user_name,
                            Employee.user_principal_name,
                        )
                    ]
                )
            )
        total = (
            self._session.scalar(
                select(func.count()).select_from(Employee).where(*predicates),
            )
            or 0
        )
        rows = self._session.scalars(
            select(Employee)
            .where(*predicates)
            .order_by(Employee.name, Employee.id)
            .offset(offset)
            .limit(limit),
        ).all()
        return list(rows), total

    def set_purchase_limit(self, employee_id: int, amount: Decimal) -> bool:
        employee = self._session.scalar(
            select(Employee)
            .where(Employee.id == employee_id)
            .with_hint(Employee, "WITH (UPDLOCK)", dialect_name="mssql")
            .execution_options(populate_existing=True),
        )
        if employee is None:
            return False
        # SQLAlchemy updates only this changed attribute. Avoid OUTPUT/RETURNING
        # rowcount assumptions, including with SQL Server pyodbc drivers.
        employee.purchase_limit = amount
        return True
