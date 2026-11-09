from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime, timezone
import time


class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: datetime
    uptime_seconds: float
    environment: str


class ReadyResponse(BaseModel):
    status: str
    timestamp: datetime


# Track startup time for uptime calculation
_startup_time = time.monotonic()


router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.now(timezone.utc),
        uptime_seconds=time.monotonic() - _startup_time,
        environment="development",
    )


@router.get("/ready", response_model=ReadyResponse)
async def readiness_check() -> ReadyResponse:
    # In a real app, this would check database connectivity, dependent services, etc.
    return ReadyResponse(
        status="ready",
        timestamp=datetime.now(timezone.utc),
    )
