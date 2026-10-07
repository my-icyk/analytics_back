from app.domains.counter_update import CounterExceptions
from app.exceptions.exceptions import NotFoundError
from app.repositories.counter_update_repository import CounterUpdateRepository
from app.schemas.counter_update_schema import (
    CounterExceptionsCreate,
    CounterExceptionsUpdate,
)


class CounterUpdateService:
    def __init__(self, repo: CounterUpdateRepository):
        self.repository = repo

    def get_by_id(
        self,
        exception_id: int,
    ) -> CounterExceptions:
        row = self.repository.get_by_id(exception_id)
        if row is None:
            raise NotFoundError("counters_update", "id", str(exception_id))
        return row

    def get_exceptions(
        self,
        counter_id: int | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[CounterExceptions]:
        return self.repository.get_all(
            counter_id=counter_id, limit=limit, offset=offset
        )

    def count_exceptions(self, counter_id: int | None = None) -> int:
        return self.repository.count(counter_id=counter_id)

    def create(self, data: CounterExceptionsCreate, user_id: int) -> None:
        # TODO: NEED TO ADD VALIDATION
        self.repository.create(
            counter_id=data.counter_id,
            valid_from=data.valid_from,
            valid_to=data.valid_to,
            visitors=data.visitors,
            is_auto=data.is_auto,
            reason=data.reason,
            created_by_user_id=user_id,
        )

    # TODO: dont like the schema CountersUpdateCreate poate se poate command sau altceva
    def update(self, exception_id: int, data: CounterExceptionsUpdate) -> None:
        self.get_by_id(exception_id)

        self.repository.update(
            exception_id=exception_id,
            counter_id=data.counter_id,
            valid_from=data.valid_from,
            valid_to=data.valid_to,
            visitors=data.visitors,
            is_auto=data.is_auto,
            reason=data.reason,
        )

    def delete(self, exception_id: int) -> None:
        self.get_by_id(exception_id)

        self.repository.delete(exception_id=exception_id)

    def get_counters(self):
        return self.repository.get_counters()

    def get_by_counter_id(self, counter_id: int) -> list[CounterExceptions]:
        return self.repository.get_by_counter_id(counter_id)
