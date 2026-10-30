from pydantic import computed_field, field_validator

from app.filters.base import PaginationParams


class DepartmentRepartitionFilter(PaginationParams):
    department_ids: list[int] | None = None
    group_ids: list[int] | None = None


class GroupFilter(PaginationParams):
    search: str | None = None
    division_ids: list[int] | None = None
    group_type_ids: list[int] | None = None

    @field_validator("search")
    @classmethod
    def normalize_search(cls, v: str | None) -> str | None:
        v = (v or "").strip()
        return v or None  # "" and "   " become None

    @computed_field
    @property
    def search_pattern(self) -> str | None:
        if not self.search:
            return None
        escaped = (
            self.search.replace("\\", "\\\\")
            .replace("%", "\\%")
            .replace("_", "\\_")
            .replace("[", "\\[")  # SQL Server treats [] as a wildcard set
        )
        return f"%{escaped}%"
