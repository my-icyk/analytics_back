from datetime import date, datetime

from pydantic import BaseModel


class CountersRead(BaseModel):
    id: int
    exception_count: int
    last_change: datetime


class CounterExceptionsView(BaseModel):
    id: int
    counter_id: int
    valid_from: date
    valid_to: date
    visitors: int
    is_auto: bool
    reason: str | None = None
    created_by: str
    created_at: datetime
    updated_at: datetime


# TODO: Actions must be provides in other places?
class CounterExceptionsCreate(BaseModel):
    counter_id: int
    valid_from: date
    valid_to: date
    visitors: int
    is_auto: bool
    reason: str | None = None


class CounterExceptionsUpdate(CounterExceptionsCreate):
    pass
