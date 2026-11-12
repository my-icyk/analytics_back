from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.db.models.employees.credit import CreditStatus

Money = Annotated[Decimal, Field(gt=0, max_digits=18, decimal_places=2)]
NonnegativeMoney = Annotated[Decimal, Field(ge=0, max_digits=18, decimal_places=2)]
PositiveId = Annotated[int, Field(gt=0, le=9223372036854775807)]


class InputModel(BaseModel):
    # Reject attempts to write synchronized employee fields or set status directly.
    model_config = ConfigDict(extra="forbid")


class CreditTerms(InputModel):
    credit_amount: Money
    nr_months: int = Field(gt=0, le=2147483647)
    start_month: date
    comments: str | None = Field(default=None, max_length=500)

    @field_validator("start_month")
    @classmethod
    def first_day(cls, value: date) -> date:
        if value.day != 1:
            raise ValueError("start_month must be the first day of a month")
        return value

    @model_validator(mode="after")
    def schedule_fits_dates(self):
        available_months = (
            (9999 - self.start_month.year) * 12 + 13 - self.start_month.month
        )
        if self.nr_months > available_months:
            raise ValueError("schedule extends beyond year 9999")
        # Preserve exactly nr_months positive rows after rounding to cents.
        if self.credit_amount < Decimal("0.01") * self.nr_months:
            raise ValueError("credit_amount must allow at least 0.01 per month")
        return self


class CreditCreate(CreditTerms):
    employee_id: PositiveId


class CreditUpdate(CreditTerms):
    """PUT replaces all editable terms; employee_id and status are immutable here."""


class CreditPayOff(InputModel):
    paid_off_on: date


class PurchaseLimitUpdate(InputModel):
    purchase_limit: NonnegativeMoney


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class EmployeeSummary(ORMModel):
    id: int
    name: str | None
    employee_ref: str | None
    department_name: str | None


class EmployeeRead(EmployeeSummary):
    user_principal_name: str | None
    fiscal_code: str | None
    user_name: str | None
    purchase_limit: Decimal | None


class RepartitionRead(ORMModel):
    end_of_month: date
    remaining_amount: Decimal


class CreditRead(ORMModel):
    id: int
    employee_id: int
    employee: EmployeeSummary
    credit_amount: Decimal
    nr_months: int
    start_month: date
    status: CreditStatus
    paid_off_on: date | None
    comments: str | None
    created_at: datetime
    created_by: int | None
    updated_at: datetime | None


class CreditDetail(CreditRead):
    repartitions: list[RepartitionRead]


class EmployeeDebtRead(BaseModel):
    employee_id: int
    end_of_month: date
    remaining_amount: Decimal


T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    items: list[T]
    total: int
    limit: int
    offset: int
