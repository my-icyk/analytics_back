from datetime import date

from pydantic import BaseModel


class DepartmentRepartitionDetails(BaseModel):
    id: int
    department_id: int
    department_name: str
    valid_from: date
    valid_to: date | None
    is_active: bool
    group_id: int
