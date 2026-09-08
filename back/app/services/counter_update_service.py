from app.core.permisions import PermissionEnum, has_permission
from app.exceptions.exceptions import ForbiddenError, NotFoundError
from app.models.counter_update import CounterUpdate
from app.models.user import User
from app.repositories.counter_update_repository import CounterUpdateRepository
from app.schemas.counter_update_schema import (
    CounterUpdateListQuery,
    CounterUpdateListResponse,
    CounterUpdateViewSchema,
)


class CounterUpdateService:
    def __init__(self, repo: CounterUpdateRepository):
        self.repository = repo

    def get_by_id(self, counter_update_id: int, current_user: User) -> CounterUpdate:
        if not has_permission(current_user, PermissionEnum.COUNTERS_UPDATE_READ):
            raise ForbiddenError("You do not have permission to read counter updates.")
        row = self.repository.get_by_id(counter_update_id)
        if row is None:
            raise NotFoundError("counters_update", "id", counter_update_id)
        return row

    def get_all(
        self, current_user: User, query: CounterUpdateListQuery
    ) -> CounterUpdateListResponse:
        if not has_permission(current_user, PermissionEnum.COUNTERS_UPDATE_READ):
            raise ForbiddenError("You do not have permission to read counter updates.")

        items, next_cursor = self.repository.get_all(
            **query.model_dump(exclude_none=True)
        )
        view_items = [
            CounterUpdateViewSchema.model_validate(item, from_attributes=True)
            for item in items
        ]

        return CounterUpdateListResponse(items=view_items, next_cursor=next_cursor)
