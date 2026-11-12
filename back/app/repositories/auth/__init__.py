# app/repositories/auth/__init__.py
from .authorization_repository import AuthorizationRepository
from .user_repository import UserRepository

__all__ = ["UserRepository", "AuthorizationRepository"]
