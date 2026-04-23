"""Top-level API router."""

from fastapi import APIRouter

from app.api.routes.auth import router as auth_router
from app.api.routes.health import router as health_router


api_router = APIRouter()
api_router.include_router(health_router, prefix="/health", tags=["health"])
<<<<<<< HEAD
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(courses_router, prefix="/courses", tags=["courses"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(progress_router, prefix="/courses", tags=["progress"])
=======
>>>>>>> 222bbae44c90e5779ca5509cd3109377ee79dce9
