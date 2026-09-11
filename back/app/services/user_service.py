from app.core.security import get_password_hash, validate_password_strength
from app.domains.user import User
from app.exceptions.exceptions import UserNotFoundError
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user(self, user_id: int) -> User:

        user = self.user_repository.get_by_id(user_id)

        if user is None:
            raise UserNotFoundError(user_id)

        return user

    def create_user(self, username: str, password: str) -> User:
        validate_password_strength(password)
        hashed = get_password_hash(password)
        return self.user_repository.create(username=username, hashed_password=hashed)

    def delete_user(self, user_id: int) -> None:

        user = self.user_repository.get_by_id(user_id)

        if user is None:
            raise UserNotFoundError(user_id)

        self.user_repository.delete(user_id)

    def update_user(self, user_id: int, username: str) -> User:
        self.get_user(user_id)
        # TODO: Need Check for username and i think for email
        return self.user_repository.update_user(user_id, username)

    def get_all_users(self) -> list[User]:
        return self.user_repository.get_all_users()

    def set_admin(self, user_id: int) -> User:
        self.get_user(user_id)

        return self.user_repository.set_admin(user_id)

    def revoke_admin(self, user_id: int) -> User:

        self.get_user(user_id)
        return self.user_repository.revoke_admin(user_id)
