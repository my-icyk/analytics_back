from pydantic import BaseModel


class PaginatedResponse[T](BaseModel):
    data: list[T]
    total: int
    success: bool = True


class IdResponse(BaseModel):
    id: int
