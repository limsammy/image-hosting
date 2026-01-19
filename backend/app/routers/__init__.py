"""
API route handlers.
"""

from app.routers.admin import router as admin_router
from app.routers.auth import router as auth_router
from app.routers.images import router as images_router

__all__ = ["admin_router", "auth_router", "images_router"]
