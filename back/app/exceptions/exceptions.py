from datetime import date


class InvalidCredentialsError(Exception):
    def __init__(self):
        super().__init__("Invalid name or password")


class InvalidTokenError(Exception):
    def __init__(self):
        super().__init__("Invalid or expired token")


class InactiveUserError(Exception):
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f"User {user_id} is inactive")


class UserNotFoundError(Exception):
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f"User with id: {user_id} not found")


class ForbiddenError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class RoleNotFoundError(Exception):
    def __init__(self, role_id: int):
        self.role_id = role_id
        super().__init__(f"Role with id: {role_id} not found")


class NotFoundError(Exception):
    def __init__(
        self,
        entity: str,
        field: str,
        value: str,
    ):
        self.entity = entity
        self.field = field
        self.value = value

        super().__init__(f"{entity} with {field}: {value} not found")


class AlreadyExistsError(Exception):
    def __init__(self, entity: str, field: str, value: str):
        self.entity = entity
        self.field = field
        self.value = value

        super().__init__(f"{entity} with {field}: '{value}' already exists")


class PasswordMismatchError(Exception):
    def __init__(self):
        super().__init__(
            "Password must contain uppercase, lowercase, and digit characters"
        )


class DeleteProtectedError(Exception):
    def __init__(
        self,
        entity: str,
        reason: str,
    ):
        self.entity = entity
        self.reason = reason

        super().__init__(f"{entity} cannot be deleted: {reason}")


class OverlappingPeriodError(Exception):
    def __init__(
        self,
        entity_name: str,
        valid_from: date,
        valid_to: date | None,
    ):
        super().__init__(
            f"{entity_name} has an overlapping period: {valid_from} - {valid_to}"
        )
