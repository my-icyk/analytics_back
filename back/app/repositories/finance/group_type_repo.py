from sqlalchemy import func, select
from sqlalchemy.orm import Session, with_expression

from app.db.models.finance import Group, GroupType


class GroupTypeRepo:
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> GroupType | None:
        return self._session.get(GroupType, id)

    def get_all(self) -> list[GroupType]:
        group_count = (
            select(func.count(Group.id))
            .where(Group.group_type_id == GroupType.id)
            .correlate(GroupType)
            .scalar_subquery()
        )

        stmt = (
            select(GroupType)
            .options(with_expression(GroupType.group_count, group_count))
            .execution_options(populate_existing=True)
            .order_by(GroupType.id)
        )
        return list(self._session.scalars(stmt))
