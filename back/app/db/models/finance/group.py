from sqlalchemy import (
    CheckConstraint,
    Computed,
    ForeignKey,
    ForeignKeyConstraint,
    Identity,
    Integer,
    Unicode,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, query_expression

from app.db.base import Base


class GroupType(Base):
    __tablename__ = "dimGroupTypes"
    __table_args__ = {"schema": "finance"}

    id: Mapped[int] = mapped_column(
        Integer, Identity(start=1, increment=1), primary_key=True
    )
    name: Mapped[str] = mapped_column(Unicode(200))
    group_count: Mapped[int | None] = query_expression()


class Group(Base):
    __tablename__ = "dimGroups"
    __table_args__ = (
        UniqueConstraint("id", "group_type_id", name="UQ_dimGroups_id_type"),
        ForeignKeyConstraint(
            ["parent_id", "parent_type_id"],
            ["finance.dimGroups.id", "finance.dimGroups.group_type_id"],
            name="FK_dimGroups_parent",
        ),
        CheckConstraint(
            "group_type_id <> 4 OR parent_id IS NULL",
            name="CK_dimGroups_folder_no_parent",
        ),
        {"schema": "finance"},
    )

    id: Mapped[int] = mapped_column(
        Integer, Identity(start=1, increment=1), primary_key=True
    )
    name: Mapped[str] = mapped_column(Unicode(255))
    division_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("finance.dimDivision.id")
    )
    group_type_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("finance.dimGroupTypes.id", name="FK_dimGroups_dimGroupTypes"),
        server_default=text("1"),
    )
    parent_id: Mapped[int | None] = mapped_column(Integer)
    parent_type_id: Mapped[int | None] = mapped_column(
        Integer,
        Computed("CASE WHEN parent_id IS NOT NULL THEN 4 END", persisted=True),
    )
    division_name: Mapped[str | None] = query_expression()

    group_type_name: Mapped[str | None] = query_expression()
    parent_name: Mapped[str | None] = query_expression()
    rules_count: Mapped[int | None] = query_expression()
    repartitions_count: Mapped[int | None] = query_expression()
