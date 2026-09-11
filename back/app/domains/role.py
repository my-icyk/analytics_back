from app.domains.domain_model import DomainModel


class Role(DomainModel):
    id: int
    name: str
    description: str | None
