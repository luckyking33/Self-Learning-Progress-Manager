"""FastAPI application entrypoint."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.db.session import engine
from models import Base


def create_application() -> FastAPI:
    # 创建所有数据库表
    Base.metadata.create_all(bind=engine)
    
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/", tags=["root"])
    async def read_root() -> dict[str, str]:
        return {"message": "STAR API is running"}

    app.include_router(api_router, prefix=settings.api_v1_prefix)
    return app


app = create_application()
