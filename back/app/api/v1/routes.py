from fastapi import APIRouter

from app.api.v1.endpoints import auth, health, permissions, roles, user_roles, users

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(health.router)
api_router.include_router(users.router)
api_router.include_router(roles.router)
api_router.include_router(permissions.router)
api_router.include_router(user_roles.router)
