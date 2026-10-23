from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import health
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize DB, connections, etc.
    yield
    # Shutdown: cleanup


def create_app() -> FastAPI:
    app = FastAPI(
        title="Cobalt Workbench",
        description="Scale computer-use 2.0 with open-source drivers, cross-OS sandboxes, and benchmarks",
        version="1.0.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router, prefix="/api/v1")

    return app


app = create_app()