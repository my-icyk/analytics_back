from decimal import Decimal

from sqlalchemy import BigInteger, Numeric, Unicode
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Employee(Base):
    """Existing, procedure-managed table. Confirm types using its real DDL.

    Do not create/migrate this table from this reference mapping. If Employee
    already exists in your app, extend/reuse that model rather than defining two.
    """

    __tablename__ = "core_employee"
    __table_args__ = {"schema": "dbo"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    name: Mapped[str | None] = mapped_column(Unicode(255))
    employee_ref: Mapped[str | None] = mapped_column(Unicode(255))
    user_principal_name: Mapped[str | None] = mapped_column(Unicode(255))
    fiscal_code: Mapped[str | None] = mapped_column(Unicode(255))
    department_name: Mapped[str | None] = mapped_column(Unicode(255))
    user_name: Mapped[str | None] = mapped_column(Unicode(255))
    purchase_limit: Mapped[Decimal | None] = mapped_column(Numeric(18, 2))
