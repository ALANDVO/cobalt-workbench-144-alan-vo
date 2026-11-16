from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any

from app.core.drivers.docker import DockerDriver

router = APIRouter(tags=["sandbox"])


# Models
class SandboxCreateRequest(BaseModel):
    name: Optional[str] = None
    config: Optional[Dict[str, Any]] = None


class SandboxResponse(BaseModel):
    id: str
    name: Optional[str] = None
    driver: str
    status: str
    config: Optional[Dict[str, Any]] = None
    created_at: float


class SandboxActionResponse(BaseModel):
    id: str
    status: str
    message: str


# Driver instance (singleton) - can be configured elsewhere
_driver = DockerDriver()


@router.post("/sandboxes", response_model=SandboxResponse)
async def create_sandbox(request: SandboxCreateRequest) -> SandboxResponse:
    sandbox = _driver.create(name=request.name, config=request.config)
    return SandboxResponse(id=sandbox.id, name=sandbox.name, driver=sandbox.driver, status=sandbox.status, config=sandbox.config, created_at=sandbox.created_at)


@router.post("/sandboxes/{sandbox_id}/start", response_model=SandboxActionResponse)
async def start_sandbox(sandbox_id: str) -> SandboxActionResponse:
    try:
        sandbox = _driver.start(sandbox_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return SandboxActionResponse(id=sandbox.id, status=sandbox.status, message="Sandbox started")


@router.post("/sandboxes/{sandbox_id}/stop", response_model=SandboxActionResponse)
async def stop_sandbox(sandbox_id: str) -> SandboxActionResponse:
    try:
        sandbox = _driver.stop(sandbox_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return SandboxActionResponse(id=sandbox.id, status=sandbox.status, message="Sandbox stopped")


@router.delete("/sandboxes/{sandbox_id}", response_model=SandboxActionResponse)
async def destroy_sandbox(sandbox_id: str) -> SandboxActionResponse:
    if not _driver.destroy(sandbox_id):
        raise HTTPException(status_code=404, detail=f"Sandbox not found: {sandbox_id}")
    return SandboxActionResponse(id=sandbox_id, status="destroyed", message="Sandbox destroyed")
