from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.finance import Division


class DivisionRepo:
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, division_id: int) -> Division | None:
        return self._session.get(Division, division_id)

    def get_by_name(self, name: str) -> Division | None:
        stmt = select(Division).where(Division.name == name)
        return self._session.scalar(stmt)

    def get_all(self) -> list[Division]:
        stmt = select(Division).order_by(Division.name, Division.id)
        return list(self._session.scalars(stmt))

    def create(self, name: str, is_administrative: bool, company_id: int | None) -> int:
        division = Division(
            name=name,
            is_administrative=is_administrative,
            company_id=company_id,
        )
        self._session.add(division)
        self._session.flush()
        return division.id

    def delete(self, division: Division) -> None:
        self._session.delete(division)
