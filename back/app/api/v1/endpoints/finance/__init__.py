from fastapi import APIRouter

from . import companies, department_repartitions

router = APIRouter(prefix="/finance")

router.include_router(
    department_repartitions.router,
    prefix="/department-repartitions",
    tags=["finance"],
)
router.include_router(
    companies.router,
    prefix="/companies",
    tags=["finance"],
)
