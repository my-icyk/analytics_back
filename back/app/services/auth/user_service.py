from sqlalchemy import RowMapping
from sqlalchemy.orm import Session

from app.core.security import (
    get_password_hash,
    validate_password_strength,
    verify_password,
)
from app.db.models.auth import User
from app.exceptions.exceptions import (
    AlreadyExistsError,
    BadRequestError,
    ForbiddenError,
    NotFoundError,
)
from app.repositories.auth import UserRepo
from app.services.common import WriteService


class UserService(WriteService):
    def __init__(self, session: Session, *, user_repo: UserRepo):
        super().__init__(session)
        self._users = user_repo

    def _get_active_user(self, user_id: int) -> User:
        user = self.get_user(user_id)  # raises NotFound if missing
        if not user.is_active:
            raise ForbiddenError("User is inactive")
        return user

    def get_user(self, user_id: int) -> User:

        user = self._users.get_by_id(user_id)

        if user is None:
            raise NotFoundError(entity="User", field="id", value=str(user_id))

        return user

    def get_employee_details(self, user: User) -> RowMapping | None:
        if user.employee_ref is None:
            return None

        return self._users.get_employee_details(user.employee_ref)

    def create_user(
        self, username: str, password: str, name: str, email: str | None = None
    ) -> User:
        validate_password_strength(password)
        hashed_password = get_password_hash(password)

        with self._write():
            user = self._users.create(
                username=username,
                hashed_password=hashed_password,
                name=name,
                email=email,
            )
        return user

    def delete_user(self, user_id: int) -> None:
        with self._write():
            user = self.get_user(user_id)
            self._users.delete(user)

    def update_user(
        self,
        user_id: int,
        username: str,
        email: str | None,
        is_active: bool,
        name: str,
    ) -> User:
        with self._write():
            user = self.get_user(user_id)
            user.username = username
            user.email = email
            user.is_active = is_active
            user.name = name
        return user

    def get_all_users(self) -> list[User]:
        return self._users.get_all_users()

    def set_admin_status(self, user_id: int, *, is_admin: bool) -> User:
        with self._write():
            user = self.get_user(user_id)
            user.is_admin = is_admin
        return user

    def change_own_password(
        self, user: User, current_password: str, new_password: str
    ) -> None:
        with self._write():
            if not verify_password(current_password, user.hashed_password):
                raise ForbiddenError("Current password is incorrect")

            self._set_password(user, new_password)

    def reset_password(self, caller: User, user_id: int, new_password: str) -> None:
        if not caller.is_admin:
            raise ForbiddenError("You can't reset this user's password")

        with self._write():
            user = self._get_active_user(user_id)
            self._set_password(user, new_password)

    def _set_password(self, user: User, new_password: str) -> None:
        validate_password_strength(new_password)

        if verify_password(new_password, user.hashed_password):
            raise BadRequestError("New password must be different from the current one")

        user.hashed_password = get_password_hash(new_password)

    def create_admin_user(self, username: str, password: str, name: str) -> User:
        validate_password_strength(password)
        hashed_password = get_password_hash(password)

        with self._write():
            if self._users.get_by_username(username) is not None:
                raise AlreadyExistsError("User", "username", username)

            user = self._users.create(
                username=username,
                hashed_password=hashed_password,
                name=name,
            )
            user.is_admin = True

        return user
