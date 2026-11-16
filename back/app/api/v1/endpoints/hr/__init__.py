from fastapi import APIRouter

from . import credits, employees

router = APIRouter(prefix="/hr", tags=["hr"])

router.include_router(
    employees.router,
    prefix="/employees",
)
router.include_router(
    credits.router,
    prefix="/credits",
)
