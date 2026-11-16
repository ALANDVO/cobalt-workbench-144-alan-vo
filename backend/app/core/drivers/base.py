from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Optional, List


@dataclass
class Sandbox:
    id: str
    name: Optional[str] = None
    driver: str = ""
    status: str = "pending"
    config: Optional[Dict[str, Any]] = None
    created_at: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "driver": self.driver,
            "status": self.status,
            "config": self.config,
            "created_at": self.created_at,
        }


class SandboxDriver(ABC):
    """Abstract interface for sandbox drivers (Docker, Lume, etc.)."""

    @abstractmethod
    def create(self, name: Optional[str] = None, config: Optional[Dict[str, Any]] = None) -> Sandbox:
        """Create a new sandbox. Returns a Sandbox instance with a generated ID and initial status."""
        pass

    @abstractmethod
    def start(self, sandbox_id: str) -> Sandbox:
        """Start the sandbox with given ID. Returns updated Sandbox."""
        pass

    @abstractmethod
    def stop(self, sandbox_id: str) -> Sandbox:
        """Stop the sandbox with given ID. Returns updated Sandbox."""
        pass

    @abstractmethod
    def destroy(self, sandbox_id: str) -> bool:
        """Destroy the sandbox with given ID. Returns True on success."""
        pass

    @abstractmethod
    def get(self, sandbox_id: str) -> Optional[Sandbox]:
        """Retrieve sandbox by ID. Returns Sandbox or None if not found."""
        pass

    @abstractmethod
    def list(self) -> List[Sandbox]:
        """List all sandboxes."""
        pass
