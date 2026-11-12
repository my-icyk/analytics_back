from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.auth import User


class UserRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, user_id: int) -> User | None:
        return self._session.get(User, user_id)

    def get_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        return self._session.scalar(stmt)

    def get_all_users(self) -> list[User]:
        stmt = select(User).order_by(User.id)
        return list(self._session.scalars(stmt).all())

    def create(
        self,
        username: str,
        hashed_password: str,
        name: str,
        email: str | None = None,
    ) -> User:
        user = User(
            username=username,
            hashed_password=hashed_password,
            name=name,
            email=email,
        )
        self._session.add(user)
        self._session.flush()
        return user
