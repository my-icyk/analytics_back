from fastapi import APIRouter

from . import (
    companies,
    department_repartitions,
    divisions,
    group_rules,
    groups,
    snapshots,
)

router = APIRouter(prefix="/finance")

router.include_router(
    department_repartitions.router,
    prefix="/department-repartitions",
    tags=["department-repartitions"],
)
router.include_router(
    companies.router,
    prefix="/companies",
    tags=["companies"],
)
router.include_router(
    divisions.router,
    prefix="/divisions",
    tags=["divisions"],
)
router.include_router(
    groups.router,
    prefix="/groups",
    tags=["groups"],
)
router.include_router(
    group_rules.router,
    prefix="/groups/{group_id}/rules",
    tags=["group-rules"],
)
router.include_router(
    snapshots.router,
    prefix="/snapshots",
    tags=["snapshots"],
)
