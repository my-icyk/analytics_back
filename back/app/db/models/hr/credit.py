from datetime import date, datetime
from decimal import Decimal
from enum import StrEnum

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Unicode,
    func,
)
from sqlalchemy.dialects.mssql import DATETIME2
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.hr.employee import Employee


class CreditStatus(StrEnum):
    ACTIVE = "active"
    PAID_OFF = "paid_off"
    CANCELLED = "cancelled"


class EmployeeCredit(Base):
    __tablename__ = "employee_credit"
    __table_args__ = (
        CheckConstraint("credit_amount > 0", name="CK_employee_credit_amount"),
        CheckConstraint("nr_months > 0", name="CK_employee_credit_months"),
        CheckConstraint("DAY(start_month) = 1", name="CK_employee_credit_start").ddl_if(
            dialect="mssql"
        ),
        CheckConstraint(
            "status IN ('active', 'paid_off', 'cancelled')",
            name="CK_employee_credit_status",
        ),
        CheckConstraint(
            "(status = 'paid_off' AND paid_off_on IS NOT NULL "
            "AND paid_off_on >= start_month) OR "
            "(status IN ('active', 'cancelled') AND paid_off_on IS NULL)",
            name="CK_employee_credit_paid_off",
        ),
        {"schema": "hr"},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("dbo.core_employee.id"))
    credit_amount: Mapped[Decimal] = mapped_column(Numeric(18, 2))
    nr_months: Mapped[int] = mapped_column(Integer)
    start_month: Mapped[date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(
        String(20),
        default=CreditStatus.ACTIVE.value,
        server_default="active",
    )
    paid_off_on: Mapped[date | None] = mapped_column(Date)
    comments: Mapped[str | None] = mapped_column(Unicode(500))
    created_at: Mapped[datetime] = mapped_column(
        DateTime().with_variant(DATETIME2(precision=0), "mssql"),
        server_default=func.current_timestamp(),
    )
    created_by: Mapped[int | None] = mapped_column(ForeignKey("api.users.id"))
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime().with_variant(DATETIME2(precision=0), "mssql"),
    )

    employee: Mapped[Employee] = relationship(lazy="raise")
    repartitions: Mapped[list["CreditRepartition"]] = relationship(
        back_populates="credit",
        order_by="CreditRepartition.end_of_month",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="raise",
    )


class CreditRepartition(Base):
    __tablename__ = "employee_credit_repartition"
    __table_args__ = (
        CheckConstraint(
            "remaining_amount >= 0",
            name="CK_employee_credit_repartition_amount",
        ),
        CheckConstraint(
            "end_of_month = EOMONTH(end_of_month)",
            name="CK_credit_repartition_month_end",
        ).ddl_if(dialect="mssql"),
        {"schema": "hr"},
    )

    credit_id: Mapped[int] = mapped_column(
        ForeignKey("hr.employee_credit.id", ondelete="CASCADE"),
        primary_key=True,
    )
    end_of_month: Mapped[date] = mapped_column(Date, primary_key=True)
    remaining_amount: Mapped[Decimal] = mapped_column(Numeric(18, 2))

    credit: Mapped[EmployeeCredit] = relationship(back_populates="repartitions")
