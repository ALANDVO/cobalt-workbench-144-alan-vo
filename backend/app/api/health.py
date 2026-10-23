from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime, timezone


class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: datetime


router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.now(timezone.utc),
    )