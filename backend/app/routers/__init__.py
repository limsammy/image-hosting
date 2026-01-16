"""
API route handlers.
"""

from app.routers.auth import router as auth_router
from app.routers.images import router as images_router

__all__ = ["auth_router", "images_router"]
