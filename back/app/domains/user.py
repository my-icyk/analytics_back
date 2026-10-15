from app.domains.domain_model import DomainModel


class User(DomainModel):
    id: int
    name: str
    email: str | None = None
    username: str
    is_active: bool
    is_admin: bool
    hashed_password: str
