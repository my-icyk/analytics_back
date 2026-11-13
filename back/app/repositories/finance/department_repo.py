from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.db.models.finance import Department
from app.repositories.base import LookupResponse


class DepartmentRepo:
    def __init__(self, session: Session):
        self._session = session

    def get_all(self) -> list[Department]:
        stmt = select(Department).order_by(
            Department.brand, Department.name, Department.id
        )
        return list(self._session.scalars(stmt))

    def lookup(self, search: str | None) -> list[LookupResponse]:
        rows = self._session.execute(
            text("EXEC api.sp_lookup_departments @search = :search"),
            {"search": search},
        ).mappings()
        return [LookupResponse.model_validate(row) for row in rows]
