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
        value: int,
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

        super().__init__(f"{entity} with {field}: {value} already exists")
