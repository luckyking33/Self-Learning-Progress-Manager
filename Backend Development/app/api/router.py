"""Top-level API router."""

from fastapi import APIRouter

from app.api.routes.health import router as health_router
from app.api.routes.courses import router as courses_router
from app.api.routes.users import router as users_router
from app.api.routes.progress import router as progress_router


api_router = APIRouter()
api_router.include_router(health_router, prefix="/health", tags=["health"])
api_router.include_router(courses_router, prefix="/courses", tags=["courses"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(progress_router, prefix="/courses", tags=["progress"])
