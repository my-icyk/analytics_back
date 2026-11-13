from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.db.models.auth import Role, UserRole


class UserRoleRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_roles_by_user_id(self, user_id: int) -> list[Role]:
        stmt = (
            select(Role)
            .join(UserRole, UserRole.role_id == Role.id)
            .where(UserRole.user_id == user_id)
            .order_by(Role.name)
        )
        return list(self._session.scalars(stmt))

    def user_has_role(self, user_id: int, role_id: int) -> bool:
        assignment = self._session.get(
            UserRole,
            {"user_id": user_id, "role_id": role_id},
        )
        return assignment is not None

    def assign_roles(self, user_id: int, role_ids: list[int]) -> None:
        self._session.execute(delete(UserRole).where(UserRole.user_id == user_id))
        self._session.add_all(
            UserRole(user_id=user_id, role_id=role_id) for role_id in role_ids
        )
