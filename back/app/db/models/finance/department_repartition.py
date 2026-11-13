from datetime import date

from sqlalchemy import Date, ForeignKey, Identity, Integer
from sqlalchemy.orm import Mapped, mapped_column, query_expression

from app.db.base import Base


class DepartmentRepartition(Base):
    __tablename__ = "factDepartmentsRepartition"
    __table_args__ = {"schema": "finance"}

    id: Mapped[int] = mapped_column(
        Integer, Identity(start=1, increment=1), primary_key=True
    )
    department_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("finance.dimDepartments.id")
    )
    group_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("finance.dimGroups.id")
    )
    valid_from: Mapped[date] = mapped_column(Date)
    valid_to: Mapped[date | None] = mapped_column(Date)
    department_name: Mapped[str | None] = query_expression()
    department_code: Mapped[str | None] = query_expression()
    brand_name: Mapped[str | None] = query_expression()
    group_name: Mapped[str | None] = query_expression()
    is_active: Mapped[bool | None] = query_expression()
