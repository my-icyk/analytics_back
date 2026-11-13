from fastapi import APIRouter, Depends, Query

from app.api.deps import get_employee_service
from app.api.schemas.employee import EmployeeRead, Page
from app.services.employees.employee_service import EmployeeService

router = APIRouter()


@router.get("", response_model=Page[EmployeeRead])
def list_employees(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0, le=2147483647),
    search: str | None = Query(None, max_length=255),
    service: EmployeeService = Depends(get_employee_service),
):
    items, total = service.get_page(limit=limit, offset=offset, search=search)
    return Page[EmployeeRead](
        items=[EmployeeRead.model_validate(item) for item in items],
        total=total,
        limit=limit,
        offset=offset,
    )
