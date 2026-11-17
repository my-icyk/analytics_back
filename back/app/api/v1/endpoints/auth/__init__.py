from fastapi import APIRouter

from . import auth, permissions, roles, users

router = APIRouter(prefix="/auth")

router.include_router(auth.router, tags=["auth"])

router.include_router(permissions.router, prefix="/permissions", tags=["permissions"])

router.include_router(roles.router, prefix="/roles", tags=["roles"])

router.include_router(users.router, prefix="/users", tags=["users"])
