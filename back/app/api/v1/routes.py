from fastapi import APIRouter

from app.api.v1.endpoints import (
    analytics,
    auth,
    counters_update,
    employees,
    finance,
    health,
    specific,
)

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(health.router)

api_router.include_router(counters_update.counter_router)
api_router.include_router(counters_update.exceptions_router)
api_router.include_router(specific.router)
api_router.include_router(finance.router)
api_router.include_router(analytics.router)
api_router.include_router(employees.router)
