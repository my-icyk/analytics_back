from sqlalchemy import func, select, text
from sqlalchemy.orm import Session, aliased, with_expression

from app.db.models.finance import (
    DepartmentRepartition,
    Division,
    Group,
    GroupRule,
    GroupType,
)
from app.filters.finance import GroupFilter
from app.repositories.base import LookupResponse

# Only this column is needed to count repartitions. Replace this reference
# with the ORM model when we migrate DepartmentRepartitionRepository.


class GroupRepo:
    def __init__(self, session: Session):
        self._session = session

    def _details_query(self):
        parent = aliased(Group)

        rules_count = (
            select(func.count())
            .select_from(GroupRule)
            .where(GroupRule.group_id == Group.id)
            .correlate(Group)
            .scalar_subquery()
        )
        repartitions_count = (
            select(func.count())
            .select_from(DepartmentRepartition)
            .where(DepartmentRepartition.group_id == Group.id)
            .correlate(Group)
            .scalar_subquery()
        )

        return (
            select(Group)
            .join(Division, Division.id == Group.division_id)
            .join(GroupType, GroupType.id == Group.group_type_id)
            .outerjoin(parent, parent.id == Group.parent_id)
            .options(
                with_expression(Group.division_name, Division.name),
                with_expression(Group.group_type_name, GroupType.name),
                with_expression(Group.parent_name, parent.name),
                with_expression(Group.rules_count, rules_count),
                with_expression(Group.repartitions_count, repartitions_count),
            )
            .execution_options(populate_existing=True)
        )

    def get_by_id(self, id: int) -> Group | None:
        stmt = self._details_query().where(Group.id == id)
        return self._session.scalar(stmt)

    def get_by_id_light(self, id: int) -> Group | None:
        return self._session.get(Group, id)

    def get_by_name(self, name: str) -> Group | None:
        return self._session.scalar(select(Group).where(Group.name == name))

    def get_all(self, filters: GroupFilter) -> tuple[list[Group], int]:
        conditions = []

        if filters.division_ids:
            conditions.append(Group.division_id.in_(filters.division_ids))

        if filters.group_type_ids:
            conditions.append(Group.group_type_id.in_(filters.group_type_ids))

        if filters.search_pattern:
            conditions.append(Group.name.like(filters.search_pattern, escape="\\"))

        count_stmt = select(func.count()).select_from(Group).where(*conditions)
        total = self._session.scalar(count_stmt) or 0

        page_stmt = (
            self._details_query()
            .where(*conditions)
            .order_by(Group.id)
            .offset(filters.offset)
            .limit(filters.limit)
        )
        return list(self._session.scalars(page_stmt)), total

    def get_folders(self) -> list[Group]:
        stmt = select(Group).where(Group.group_type_id == 4).order_by(Group.id)
        return list(self._session.scalars(stmt))

    def get_by_division_id_light(self, id: int) -> list[Group]:
        stmt = select(Group).where(Group.division_id == id)
        return list(self._session.scalars(stmt))

    def lookup(self, search: str | None) -> list[LookupResponse]:
        rows = self._session.execute(
            text("EXEC api.sp_lookup_groups @search = :search"),
            {"search": search},
        ).mappings()
        return [LookupResponse.model_validate(row) for row in rows]

    def create(
        self,
        name: str,
        group_type_id: int,
        division_id: int,
        parent_id: int | None = None,
    ) -> int:
        group = Group(
            name=name,
            group_type_id=group_type_id,
            division_id=division_id,
            parent_id=parent_id,
        )
        self._session.add(group)
        self._session.flush()
        return group.id

    def delete(self, group: Group) -> None:
        self._session.delete(group)
