from app.core.security import (
    get_password_hash,
    validate_password_strength,
    verify_password,
)
from app.domains.user import User
from app.exceptions.exceptions import BadRequestError, ForbiddenError, UserNotFoundError
from app.repositories.base import LookupResponse
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def _get_active_user(self, user_id: int) -> User:
        user = self.get_user(user_id)  # raises NotFound if missing
        if not user.is_active:
            raise ForbiddenError("User is inactive")
        return user

    def get_user(self, user_id: int) -> User:

        user = self.user_repository.get_by_id(user_id)

        if user is None:
            raise UserNotFoundError(user_id)

        return user

    def create_user(
        self, username: str, password: str, name: str, email: str | None = None
    ) -> User:
        validate_password_strength(password)
        hashed = get_password_hash(password)
        return self.user_repository.create(
            username=username, hashed_password=hashed, name=name, email=email
        )

    def delete_user(self, user_id: int) -> None:

        user = self.user_repository.get_by_id(user_id)

        if user is None:
            raise UserNotFoundError(user_id)

        self.user_repository.delete(user_id)

    def update_user(
        self, user_id: int, username: str, email: str | None, is_active: bool, name: str
    ) -> User:
        self.get_user(user_id)
        # TODO: Need Check for username and i think for email
        return self.user_repository.update_user(
            user_id, username, email=email, is_active=is_active, name=name
        )

    def get_all_users(self) -> list[User]:
        return self.user_repository.get_all_users()

    def set_admin(self, user_id: int) -> User:
        self.get_user(user_id)

        return self.user_repository.set_admin(user_id)

    def revoke_admin(self, user_id: int) -> User:

        self.get_user(user_id)
        return self.user_repository.revoke_admin(user_id)

    def lookup_users(self, search: str) -> list[LookupResponse]:
        return self.user_repository.lookup_users(search)

    def change_own_password(
        self, user_id: int, current_password: str, new_password: str
    ) -> None:
        user = self._get_active_user(user_id)

        if not verify_password(current_password, user.hashed_password):
            raise ForbiddenError("Current password is incorrect")

        self._set_password(user, new_password)

    def reset_password(self, caller_id: int, user_id: int, new_password: str) -> None:
        caller = self._get_active_user(caller_id)
        if not caller.is_admin:
            raise ForbiddenError("You can't reset this user's password")

        user = self._get_active_user(user_id)
        self._set_password(user, new_password)

    def _set_password(self, user: User, new_password: str) -> None:
        validate_password_strength(new_password)

        if verify_password(new_password, user.hashed_password):
            raise BadRequestError("New password must be different from the current one")

        self.user_repository.update_password(user.id, get_password_hash(new_password))
