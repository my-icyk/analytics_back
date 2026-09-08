from datetime import date

from pydantic import BaseModel, Field


class CounterUpdateViewSchema(BaseModel):
    id: int
    start_date: date
    end_date: date | None
    id_counter: int
    amount: int
    auto: bool
    comment: str | None


class CounterUpdateListResponse(BaseModel):
    items: list[CounterUpdateViewSchema]
    next_cursor: int | None = None


class CounterUpdateListQuery(BaseModel):
    cursor_id: int | None = Field(default=None, ge=1)
    id_counter: int | None = Field(default=None, ge=1)
    auto: bool | None = None
    start_date_from: date | None = None
    start_date_to: date | None = None


class CountersUpdateCreate(BaseModel):
    start_date: date
    end_date: date
    id_counter: int
    amount: int = 0
    auto: bool
    comment: str | None = None
