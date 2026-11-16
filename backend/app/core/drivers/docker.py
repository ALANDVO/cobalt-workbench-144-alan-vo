from typing import Dict, Any, Optional
import uuid
from datetime import datetime, timezone

from .base import Sandbox, SandboxDriver


class DockerDriver(SandboxDriver):
    """Driver for Docker-based sandboxes."""

    def __init__(self):
        self._sandboxes: Dict[str, Sandbox] = {}
        self._driver_name = "docker"

    def _make_sandbox(self, name: Optional[str] = None, config: Optional[Dict[str, Any]] = None) -> Sandbox:
        now = datetime.now(timezone.utc).timestamp()
        sandbox_id = str(uuid.uuid4())
        return Sandbox(
            id=sandbox_id,
            name=name,
            driver=self._driver_name,
            status="created",
            config=config,
            created_at=now,
        )

    def create(self, name: Optional[str] = None, config: Optional[Dict[str, Any]] = None) -> Sandbox:
        sandbox = self._make_sandbox(name, config)
        self._sandboxes[sandbox.id] = sandbox
        return sandbox

    def start(self, sandbox_id: str) -> Sandbox:
        sandbox = self._get(sandbox_id)
        if not sandbox:
            raise ValueError(f"Sandbox not found: {sandbox_id}")
        sandbox.status = "running"
        return sandbox

    def stop(self, sandbox_id: str) -> Sandbox:
        sandbox = self._get(sandbox_id)
        if not sandbox:
            raise ValueError(f"Sandbox not found: {sandbox_id}")
        sandbox.status = "stopped"
        return sandbox

    def destroy(self, sandbox_id: str) -> bool:
        if sandbox_id in self._sandboxes:
            del self._sandboxes[sandbox_id]
            return True
        return False

    def get(self, sandbox_id: str) -> Optional[Sandbox]:
        return self._get(sandbox_id)

    def list(self) -> list[Sandbox]:
        return list(self._sandboxes.values())

    def _get(self, sandbox_id: str) -> Optional[Sandbox]:
        return self._sandboxes.get(sandbox_id)
