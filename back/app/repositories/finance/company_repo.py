from sqlalchemy import select, true
from sqlalchemy.orm import Session

from app.db.models.finance import Company


class CompanyRepo:
    def __init__(self, session: Session):
        self._session = session

    def get_company(self, company_id: int) -> Company | None:
        return self._session.get(Company, company_id)

    def get_companies(self, only_active: bool = True) -> list[Company]:
        stmt = select(Company).order_by(Company.sort_order)
        if only_active:
            stmt = stmt.where(Company.is_active == true())
        return list(self._session.scalars(stmt))
