from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    counters_update,
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
