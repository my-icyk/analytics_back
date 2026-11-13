from sqlalchemy import delete, insert, literal, select, update
from sqlalchemy.orm import Session

from app.db.models.auth import Permission, Role, RolePermission


class RoleRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, role_id: int) -> Role | None:
        return self._session.get(Role, role_id)

    def get_all(self) -> list[Role]:
        stmt = select(Role).order_by(Role.name)
        return list(self._session.scalars(stmt).all())

    def get_by_name(self, name: str) -> Role | None:
        stmt = select(Role).where(Role.name == name)
        return self._session.scalar(stmt)

    def create(self, name: str, description: str | None = None) -> int:
        role = Role(name=name, description=description)
        self._session.add(role)
        self._session.flush()
        return role.id

    def update(self, role_id: int, name: str, description: str | None) -> None:
        stmt = (
            update(Role)
            .where(Role.id == role_id)
            .values(name=name, description=description)
        )
        self._session.execute(stmt)

    def delete(self, role_id: int) -> None:
        stmt = delete(Role).where(Role.id == role_id)
        self._session.execute(stmt)

    def assign_permissions(self, role_id: int, permission_ids: list[int]) -> None:
        self._session.execute(
            delete(RolePermission).where(RolePermission.role_id == role_id)
        )

        if not permission_ids:
            return

        permissions_to_assign = select(literal(role_id), Permission.id).where(
            Permission.id.in_(permission_ids)
        )
        stmt = insert(RolePermission).from_select(
            ["role_id", "permission_id"],
            permissions_to_assign,
        )
        self._session.execute(stmt)

    def get_existing_ids(self, ids: list[int]) -> set[int]:
        if not ids:
            return set()

        stmt = select(Role.id).where(Role.id.in_(ids))
        return set(self._session.scalars(stmt))
