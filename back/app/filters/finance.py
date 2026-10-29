from app.filters.base import PaginationParams


class DepartmentRepartitionFilter(PaginationParams):
    department_ids: list[int] | None = None
    group_ids: list[int] | None = None


class GroupFilter(PaginationParams):
    search: str | None = None
    division_ids: list[int] | None = None
    group_type_ids: list[int] | None = None
