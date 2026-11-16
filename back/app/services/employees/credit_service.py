from datetime import date
from decimal import InvalidOperation

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.schemas.hr import CreditCreate, CreditUpdate
from app.db.models.hr import CreditStatus, EmployeeCredit
from app.exceptions.exceptions import NotFoundError
from app.repositories.employees import CreditRepository, EmployeeRepository
from app.services.common import Conflict, WriteService
from app.utils import generate_schedule


class CreditService(WriteService):
    def __init__(
        self,
        session: Session,
        *,
        credit_repo: CreditRepository,
        employee_repo: EmployeeRepository,
    ):
        super().__init__(session)
        self._credits = credit_repo
        self._employees = employee_repo

    def get(self, credit_id: int) -> EmployeeCredit:
        credit = self._credits.get_by_id(credit_id)
        if credit is None:
            raise NotFoundError(entity="Credit", field="id", value=str(credit_id))
        return credit

    def get_page(
        self,
        *,
        limit: int,
        offset: int,
        employee_id: int,
        statuses: list[CreditStatus] | None = None,
        search: str | None = None,
    ) -> tuple[list[EmployeeCredit], int]:
        return self._credits.get_page(
            limit=limit,
            offset=offset,
            employee_id=employee_id,
            statuses=statuses,
            search=search,
        )

    def _get_locked(self, credit_id: int) -> EmployeeCredit:
        credit = self._credits.get_for_update(credit_id)
        if credit is None:
            raise NotFoundError(entity="Credit", field="id", value=str(credit_id))
        return credit

    @staticmethod
    def _require_active(credit: EmployeeCredit) -> None:
        if credit.status != CreditStatus.ACTIVE.value:
            raise Conflict("Only active credits can be edited or paid off")

    def create(self, data: CreditCreate, *, employee_id: int, created_by: int) -> int:
        with self._write():
            if self._employees.get_by_id(employee_id) is None:
                raise NotFoundError(
                    entity="Employee", field="id", value=str(employee_id)
                )
            credit = EmployeeCredit(
                **data.model_dump(),
                employee_id=employee_id,
                created_by=created_by,
                status=CreditStatus.ACTIVE.value,
            )
            self._credits.add(credit)
            self._credits.replace_schedule(
                credit,
                generate_schedule(
                    data.credit_amount,
                    data.nr_months,
                    data.start_month,
                ),
            )
            credit_id = credit.id
        return credit_id

    def update(self, credit_id: int, employee_id: int, data: CreditUpdate) -> None:
        with self._write():
            credit = self._get_locked(credit_id)
            if employee_id != credit.employee_id:
                raise Conflict("Cannot update credit for a different employee")
            self._require_active(credit)
            for field, value in data.model_dump().items():
                setattr(credit, field, value)
            credit.updated_at = func.current_timestamp()
            # Deliberate policy: editing terms regenerates past and future rows.
            self._credits.replace_schedule(
                credit,
                generate_schedule(
                    credit.credit_amount,
                    credit.nr_months,
                    credit.start_month,
                ),
            )

    def pay_off(self, credit_id: int, paid_off_on: date) -> None:
        with self._write():
            credit = self._get_locked(credit_id)
            if credit.status == CreditStatus.PAID_OFF.value:
                if credit.paid_off_on != paid_off_on:
                    raise Conflict("Credit was already paid off on a different date")
                # Retrying the same request is harmless.
            else:
                self._require_active(credit)
                if paid_off_on < credit.start_month:
                    raise InvalidOperation(
                        "Repayment cannot precede the credit start month"
                    )
                credit.status = CreditStatus.PAID_OFF.value
                credit.paid_off_on = paid_off_on
                credit.updated_at = func.current_timestamp()
                self._credits.remove_schedule_from(credit, paid_off_on.replace(day=1))

    def cancel(self, credit_id: int) -> None:
        with self._write():
            credit = self._get_locked(credit_id)
            if credit.status == CreditStatus.PAID_OFF.value:
                raise Conflict("A paid-off credit cannot be cancelled")
            if credit.status != CreditStatus.CANCELLED.value:
                credit.status = CreditStatus.CANCELLED.value
                credit.updated_at = func.current_timestamp()
                self._credits.replace_schedule(credit, [])

    def delete(self, credit_id: int) -> None:
        with self._write():
            credit = self._get_locked(credit_id)
            self._credits.delete(credit)
