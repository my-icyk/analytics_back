from datetime import date

from pydantic import BaseModel


class CounterUpdate(BaseModel):
    id: int
    start_date: date
    end_date: date | None
    id_counter: int
    amount: int | None
    auto: bool
    comment: str | None
