from datetime import date, datetime

from pydantic import BaseModel


class Counters(BaseModel):
    id: int
    exception_count: int
    last_change: datetime


class CounterExceptions(BaseModel):
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
