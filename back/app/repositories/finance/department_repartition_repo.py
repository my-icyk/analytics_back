from datetime import date

from sqlalchemy import Date, and_, case, cast, func, or_, select
from sqlalchemy.orm import Session, with_expression

from app.db.models.finance import Department, DepartmentRepartition, Group
from app.filters.finance import DepartmentRepartitionFilter


class DepartmentRepartitionRepo:
    def __init__(self, session: Session):
        self._session = session

    def _details_query(self):
        today = cast(func.getdate(), Date)
        active = and_(
            DepartmentRepartition.valid_from <= today,
            or_(
                DepartmentRepartition.valid_to.is_(None),
                DepartmentRepartition.valid_to >= today,
            ),
        )

        return (
            select(DepartmentRepartition)
            .join(Department, Department.id == DepartmentRepartition.department_id)
            .join(Group, Group.id == DepartmentRepartition.group_id)
            .options(
                with_expression(DepartmentRepartition.department_name, Department.name),
                with_expression(DepartmentRepartition.department_code, Department.code),
                with_expression(DepartmentRepartition.brand_name, Department.brand),
                with_expression(DepartmentRepartition.group_name, Group.name),
                with_expression(
                    DepartmentRepartition.is_active,
                    case((active, True), else_=False),
                ),
            )
            .execution_options(populate_existing=True)
        )

    def get_all(
        self, filters: DepartmentRepartitionFilter
    ) -> tuple[list[DepartmentRepartition], int]:
        conditions = []
        if filters.department_ids:
            conditions.append(
                DepartmentRepartition.department_id.in_(filters.department_ids)
            )
        if filters.group_ids:
            conditions.append(DepartmentRepartition.group_id.in_(filters.group_ids))

        filtered = self._details_query().where(*conditions)

        # Count the same joined rows that can appear on the page.
        matching_ids = filtered.with_only_columns(
            DepartmentRepartition.id, maintain_column_froms=True
        ).subquery()
        total = (
            self._session.scalar(select(func.count()).select_from(matching_ids)) or 0
        )

        page = (
            filtered.order_by(DepartmentRepartition.id)
            .offset(filters.offset)
            .limit(filters.limit)
        )
        return list(self._session.scalars(page)), total

    def get_by_id(self, id: int) -> DepartmentRepartition | None:
        stmt = self._details_query().where(DepartmentRepartition.id == id)
        return self._session.scalar(stmt)

    def get_by_group_id(self, group_id: int) -> list[DepartmentRepartition]:
        stmt = (
            self._details_query()
            .where(DepartmentRepartition.group_id == group_id)
            .order_by(
                DepartmentRepartition.valid_from.desc(),
                DepartmentRepartition.id,
            )
        )
        return list(self._session.scalars(stmt))

    def get_for_group(self, id: int, group_id: int) -> DepartmentRepartition | None:
        stmt = select(DepartmentRepartition).where(
            DepartmentRepartition.id == id,
            DepartmentRepartition.group_id == group_id,
        )
        return self._session.scalar(stmt)

    def create(
        self,
        department_id: int,
        group_id: int,
        valid_from: date,
        valid_to: date | None,
    ) -> int:
        row = DepartmentRepartition(
            department_id=department_id,
            group_id=group_id,
            valid_from=valid_from,
            valid_to=valid_to,
        )
        self._session.add(row)
        self._session.flush()
        return row.id

    def delete(self, row: DepartmentRepartition) -> None:
        self._session.delete(row)
