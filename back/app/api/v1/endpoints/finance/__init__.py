from fastapi import APIRouter

from . import department_repartitions

router = APIRouter(prefix="/finance")

router.include_router(
    department_repartitions.router,
    prefix="/department-repartitions",
    tags=["finance"],
)
