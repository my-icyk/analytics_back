from fastapi import APIRouter

from app.api.v1.endpoints import auth, health, permissions, roles, users

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(roles.router, prefix="/roles", tags=["roles"])
api_router.include_router(
    permissions.router, prefix="/permissions", tags=["permissions"]
)
