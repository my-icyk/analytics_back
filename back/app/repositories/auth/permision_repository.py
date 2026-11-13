from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.auth import Permission


class PermissionRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_all(self) -> list[Permission]:
        stmt = select(Permission).order_by(Permission.name)
        return list(self._session.scalars(stmt))

    def get_existing_ids(self, ids: list[int]) -> set[int]:
        if not ids:
            return set()

        stmt = select(Permission.id).where(Permission.id.in_(ids))
        return set(self._session.scalars(stmt))

    def get_names(self) -> set[str]:
        return set(self._session.scalars(select(Permission.name)))

    def add_names(self, names: list[str]) -> None:
        self._session.add_all(Permission(name=name) for name in names)
