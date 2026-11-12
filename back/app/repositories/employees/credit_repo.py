from datetime import date
from decimal import Decimal

from sqlalchemy import delete, func, or_, select
from sqlalchemy.orm import Session, selectinload

from app.db.models.hr.credit import (
    CreditRepartition,
    CreditStatus,
    EmployeeCredit,
)
from app.db.models.hr.employee import Employee


class CreditRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, credit_id: int) -> EmployeeCredit | None:
        return self._session.scalar(
            select(EmployeeCredit)
            .where(EmployeeCredit.id == credit_id)
            .options(
                selectinload(EmployeeCredit.employee),
                selectinload(EmployeeCredit.repartitions),
            )
            .execution_options(populate_existing=True),
        )

    def get_for_update(self, credit_id: int) -> EmployeeCredit | None:
        # SQL Server ignores SELECT ... FOR UPDATE. Use its supported lock hint.
        # The parent lock serializes schedule edits made through this service.
        return self._session.scalar(
            select(EmployeeCredit)
            .where(EmployeeCredit.id == credit_id)
            .with_hint(EmployeeCredit, "WITH (UPDLOCK)", dialect_name="mssql")
            .execution_options(populate_existing=True),
        )

    def get_page(
        self,
        *,
        limit: int,
        offset: int,
        employee_ids: list[int] | None = None,
        statuses: list[CreditStatus] | None = None,
        search: str | None = None,
    ) -> tuple[list[EmployeeCredit], int]:
        predicates = []
        if employee_ids:
            predicates.append(EmployeeCredit.employee_id.in_(employee_ids))
        if statuses:
            predicates.append(
                EmployeeCredit.status.in_([value.value for value in statuses])
            )
        if search and search.strip():
            text = search.strip()
            predicates.append(
                or_(
                    Employee.name.contains(text, autoescape=True),
                    Employee.employee_ref.contains(text, autoescape=True),
                )
            )
        base = select(EmployeeCredit).join(EmployeeCredit.employee).where(*predicates)
        total = (
            self._session.scalar(
                select(func.count()).select_from(base.subquery()),
            )
            or 0
        )
        rows = self._session.scalars(
            base.options(selectinload(EmployeeCredit.employee))
            .order_by(EmployeeCredit.id.desc())
            .offset(offset)
            .limit(limit),
        ).all()
        return list(rows), total

    def add(self, credit: EmployeeCredit) -> None:
        self._session.add(credit)
        self._session.flush()  # Fetch IDENTITY id; does not commit.

    def replace_schedule(
        self,
        credit: EmployeeCredit,
        rows: list[tuple[date, Decimal]],
    ) -> None:
        self._session.execute(
            delete(CreditRepartition).where(CreditRepartition.credit_id == credit.id),
        )
        # Discard any previously loaded collection before inserting identical keys.
        self._session.expire(credit, ["repartitions"])
        self._session.add_all(
            [
                CreditRepartition(
                    credit_id=credit.id, end_of_month=end, remaining_amount=amount
                )
                for end, amount in rows
            ]
        )

    def remove_schedule_from(self, credit: EmployeeCredit, month_start: date) -> None:
        self._session.execute(
            delete(CreditRepartition).where(
                CreditRepartition.credit_id == credit.id,
                CreditRepartition.end_of_month >= month_start,
            )
        )
        self._session.expire(credit, ["repartitions"])

    def delete(self, credit: EmployeeCredit) -> None:
        # Explicit child deletion also works when an old FK lacks CASCADE.
        self.replace_schedule(credit, [])
        self._session.delete(credit)

    def employee_debt(self, employee_id: int, end_of_month: date) -> Decimal:
        value = self._session.scalar(
            select(func.coalesce(func.sum(CreditRepartition.remaining_amount), 0))
            .join(EmployeeCredit, EmployeeCredit.id == CreditRepartition.credit_id)
            .where(
                EmployeeCredit.employee_id == employee_id,
                CreditRepartition.end_of_month == end_of_month,
            ),
        )
        # Do not filter status='active': paid-off credits retain historical debt.
        return Decimal(value if value is not None else 0).quantize(Decimal("0.01"))
