from datetime import datetime

from app.domains.domain_model import DomainModel


class Role(DomainModel):
    id: int
    name: str
    description: str | None
    created_at: datetime
    users_count: int
    permissions_count: int
