from app.filters.base import PaginationFilter


class DepartmentRepartitionFilter(PaginationFilter):
    department_ids: list[int] | None = None
    group_ids: list[int] | None = None


class GroupFilter(PaginationFilter):
    search: str | None = None
    division_ids: list[int] | None = None
    group_type_ids: list[int] | None = None
