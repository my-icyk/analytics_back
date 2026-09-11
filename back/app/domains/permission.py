from app.domains.domain_model import DomainModel


class Permission(DomainModel):
    id: int
    name: str
