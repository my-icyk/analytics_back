from datetime import date
from decimal import Decimal

from sqlalchemy import (
    Date,
    ForeignKey,
    Identity,
    Integer,
    Numeric,
    String,
    Unicode,
    select,
    text,
)
from sqlalchemy.orm import Mapped, column_property, mapped_column

from app.db.base import Base

from .group import Group


class GroupRule(Base):
    __tablename__ = "factGroupRules"
    __table_args__ = {"schema": "finance"}

    id: Mapped[int] = mapped_column(
        Integer, Identity(start=1, increment=1), primary_key=True
    )
    name: Mapped[str] = mapped_column(Unicode(255))
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey("finance.dimGroups.id"))
    valid_from: Mapped[date] = mapped_column(Date)
    valid_to: Mapped[date | None] = mapped_column(Date)
    percent_value: Mapped[Decimal] = mapped_column(
        Numeric(5, 2), server_default=text("100.00")
    )


class GroupRuleTarget(Base):
    __tablename__ = "factGroupRulesTargets"
    __table_args__ = {"schema": "finance"}

    id: Mapped[int] = mapped_column(
        Integer, Identity(start=1, increment=1), primary_key=True
    )
    rule_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("finance.factGroupRules.id")
    )
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey("finance.dimGroups.id"))
    allocation_type: Mapped[str] = mapped_column(String(20))
    percent_value: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))

    group_name: Mapped[str] = column_property(
        select(Group.name)
        .where(Group.id == group_id)
        .correlate_except(Group)
        .scalar_subquery()
    )
