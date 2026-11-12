from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session

from app.api.schemas.employee import PurchaseLimitUpdate
from app.db.models.employees import Employee
from app.exceptions.exceptions import NotFoundError
from app.repositories.employees import CreditRepository, EmployeeRepository
from app.services.common import WriteService
from app.utils import month_end


class EmployeeService(WriteService):
    def __init__(self, session: Session):
        super().__init__(session)
        self._employees = EmployeeRepository(session)
        self._credits = CreditRepository(session)

    def get(self, employee_id: int) -> Employee:
        employee = self._employees.get_by_id(employee_id)
        if employee is None:
            raise NotFoundError(entity="Employee", field="id", value=str(employee_id))
        return employee

    def get_page(
        self,
        *,
        limit: int,
        offset: int,
        search: str | None = None,
    ) -> tuple[list[Employee], int]:
        return self._employees.get_page(limit=limit, offset=offset, search=search)

    def update_purchase_limit(
        self,
        employee_id: int,
        data: PurchaseLimitUpdate,
    ) -> Employee:
        with self._write():
            if not self._employees.set_purchase_limit(employee_id, data.purchase_limit):
                raise NotFoundError(
                    entity="Employee", field="id", value=str(employee_id)
                )
        return self.get(employee_id)

    def get_debt(self, employee_id: int, month: date) -> tuple[date, Decimal]:
        self.get(employee_id)
        end = month_end(month)
        return end, self._credits.employee_debt(employee_id, end)
