from app.domains.counter_update import CounterUpdate
from app.exceptions.exceptions import NotFoundError
from app.repositories.counter_update_repository import CounterUpdateRepository
from app.schemas.counter_update_schema import (
    CountersUpdateCreate,
    CounterUpdateListQuery,
    CounterUpdateListResponse,
    CounterUpdateView,
)


class CounterUpdateService:
    def __init__(self, repo: CounterUpdateRepository):
        self.repository = repo

    def get_by_id(
        self,
        counter_update_id: int,
    ) -> CounterUpdate:
        row = self.repository.get_by_id(counter_update_id)
        if row is None:
            raise NotFoundError("counters_update", "id", str(counter_update_id))
        return row

    def create(self, data: CountersUpdateCreate) -> None:
        # TODO: NEED TO ADD VALIDATION
        self.repository.create(
            start_date=data.start_date,
            end_date=data.end_date,
            id_counter=data.id_counter,
            amount=data.amount,
            auto=data.auto,
            comment=data.comment,
        )

    # TODO: dont like the schema CountersUpdateCreate poate se poate command sau altceva
    def update(self, counter_update_id: int, data: CountersUpdateCreate) -> None:
        self.get_by_id(counter_update_id)

        self.repository.update(
            counter_update_id=counter_update_id,
            start_date=data.start_date,
            end_date=data.end_date,
            id_counter=data.id_counter,
            amount=data.amount,
            auto=data.auto,
            comment=data.comment,
        )

    def delete(self, counter_update_id: int) -> None:
        self.get_by_id(counter_update_id)

        self.repository.delete(counter_update_id=counter_update_id)

    # TODO: dont like get all method
    def get_all(self, query: CounterUpdateListQuery) -> CounterUpdateListResponse:

        items, next_cursor = self.repository.get_all(
            **query.model_dump(exclude_none=True)
        )
        view_items = [
            CounterUpdateView.model_validate(item, from_attributes=True)
            for item in items
        ]

        return CounterUpdateListResponse(items=view_items, next_cursor=next_cursor)
