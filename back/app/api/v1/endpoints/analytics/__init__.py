from fastapi import APIRouter

from . import procedures

router = APIRouter(prefix="/analytics")

router.include_router(
    procedures.router,
    prefix="/procedures",
    tags=["analytics"],
)
