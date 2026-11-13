from sqlalchemy import (
    Boolean,
    ForeignKey,
    Identity,
    Integer,
    Unicode,
    UniqueConstraint,
    false,
    func,
    select,
)
from sqlalchemy.orm import Mapped, column_property, mapped_column

from app.db.base import Base

from .company import Company
from .group import Group


class Division(Base):
    __tablename__ = "dimDivision"
    __table_args__ = (
        UniqueConstraint("name", name="UQ_dimDivision_name"),
        {"schema": "finance"},
    )

    id: Mapped[int] = mapped_column(
        Integer, Identity(start=1, increment=1), primary_key=True
    )
    name: Mapped[str] = mapped_column(Unicode(100))
    is_administrative: Mapped[bool] = mapped_column(Boolean, server_default=false())
    company_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("finance.dimCompanies.id", name="FK_dimDivisions_company"),
    )

    company_name: Mapped[str | None] = column_property(
        select(Company.name)
        .where(Company.id == company_id)
        .correlate_except(Company)
        .scalar_subquery()
    )

    group_count: Mapped[int] = column_property(
        select(func.count(Group.id))
        .where(Group.division_id == id)
        .correlate_except(Group)
        .scalar_subquery()
    )
