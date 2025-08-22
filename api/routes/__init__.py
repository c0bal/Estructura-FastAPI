from routes.user import router as user_router
from routes.auth import router as auth_router
from routes.admin import router as admin_router

__all__ = [
    "admin_router",
    "auth_router",
    "user_router"
]
