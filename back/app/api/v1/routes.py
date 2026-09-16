from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    counters_update,
    divisions,
    group_rules,
    groups,
    health,
    permissions,
    roles,
    specific,
    users,
)

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(health.router)
api_router.include_router(users.router)
api_router.include_router(roles.router)
api_router.include_router(permissions.router)
api_router.include_router(counters_update.router)
api_router.include_router(specific.router)
api_router.include_router(divisions.router, prefix="/finance", tags=["finance"])
api_router.include_router(groups.router, prefix="/finance", tags=["finance"])
api_router.include_router(group_rules.router, prefix="/finance", tags=["finance"])
