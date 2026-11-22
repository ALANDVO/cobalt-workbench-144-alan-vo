from typing import Dict, Any, Optional, List
import uuid
import sqlite3
import os
from datetime import datetime, timezone

from .base import Sandbox, SandboxDriver


class DockerDriver(SandboxDriver):
    """Driver for Docker-based sandboxes with SQLite persistence."""

    def __init__(self):
        self._db_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "sandboxes.db")
        os.makedirs(os.path.dirname(self._db_path), exist_ok=True)
        self._sandboxes: Dict[str, Sandbox] = {}
        self._init_db()
        self._driver_name = "docker"

    def _init_db(self) -> None:
        conn = sqlite3.connect(self._db_path)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sandboxes (
                id TEXT PRIMARY KEY,
                name TEXT,
                driver TEXT,
                status TEXT,
                config TEXT,
                created_at REAL
            )
            """
        )
        conn.commit()
        conn.close()

    def _get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        return conn

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

    # ——— SandboxDriver interface ———

    def create(self, name: Optional[str] = None, config: Optional[Dict[str, Any]] = None) -> Sandbox:
        sandbox = self._make_sandbox(name, config)
        conn = self._get_conn()
        conn.execute(
            "INSERT INTO sandboxes (id, name, driver, status, config, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (sandbox.id, sandbox.name, sandbox.driver, sandbox.status, sandbox.config, sandbox.created_at),
        )
        conn.commit()
        conn.close()
        self._sandboxes[sandbox.id] = sandbox  # keep in-memory cache in sync
        return sandbox

    def start(self, sandbox_id: str) -> Sandbox:
        # Check in-memory cache first; fall through to DB if not found
        if sandbox_id in self._sandboxes:
            sandbox = self._sandboxes[sandbox_id]
            sandbox.status = "running"
            # persist
            conn = self._get_conn()
            conn.execute(
                "UPDATE sandboxes SET status = 'running' WHERE id = ?",
                (sandbox_id,),
            )
            conn.commit()
            conn.close()
            return sandbox

        # Fall back to DB
        conn = self._get_conn()
        row = conn.execute("SELECT * FROM sandboxes WHERE id = ?", (sandbox_id,)).fetchone()
        conn.close()
        if not row:
            raise ValueError(f"Sandbox not found: {sandbox_id}")
        sandbox = Sandbox(
            id=row["id"],
            name=row["name"],
            driver=row["driver"],
            status="running",
            config=row["config"],
            created_at=row["created_at"],
        )
        self._sandboxes[sandbox_id] = sandbox
        return sandbox

    def stop(self, sandbox_id: str) -> Sandbox:
        if sandbox_id in self._sandboxes:
            sandbox = self._sandboxes[sandbox_id]
            sandbox.status = "stopped"
            conn = self._get_conn()
            conn.execute(
                "UPDATE sandboxes SET status = 'stopped' WHERE id = ?",
                (sandbox_id,),
            )
            conn.commit()
            conn.close()
            return sandbox

        conn = self._get_conn()
        row = conn.execute("SELECT * FROM sandboxes WHERE id = ?", (sandbox_id,)).fetchone()
        conn.close()
        if not row:
            raise ValueError(f"Sandbox not found: {sandbox_id}")
        sandbox = Sandbox(
            id=row["id"],
            name=row["name"],
            driver=row["driver"],
            status="stopped",
            config=row["config"],
            created_at=row["created_at"],
        )
        self._sandboxes[sandbox_id] = sandbox
        return sandbox

    def destroy(self, sandbox_id: str) -> bool:
        if sandbox_id in self._sandboxes:
            self._sandboxes.pop(sandbox_id, None)
            conn = self._get_conn()
            conn.execute("DELETE FROM sandboxes WHERE id = ?", (sandbox_id,))
            conn.commit()
            conn.close()
            return True

        conn = self._get_conn()
        row = conn.execute("SELECT * FROM sandboxes WHERE id = ?", (sandbox_id,)).fetchone()
        conn.execute("DELETE FROM sandboxes WHERE id = ?", (sandbox_id,))
        conn.commit()
        conn.close()
        return False

    def get(self, sandbox_id: str) -> Optional[Sandbox]:
        # Check in-memory cache first
        if sandbox_id in self._sandboxes:
            return self._sandboxes[sandbox_id]

        # Fall back to DB
        conn = self._get_conn()
        row = conn.execute("SELECT * FROM sandboxes WHERE id = ?", (sandbox_id,)).fetchone()
        conn.close()
        if not row:
            return None
        sandbox = Sandbox(
            id=row["id"],
            name=row["name"],
            driver=row["driver"],
            status=row["status"],
            config=row["config"],
            created_at=row["created_at"],
        )
        self._sandboxes[sandbox_id] = sandbox
        return sandbox

    def list(self) -> List[Sandbox]:
        conn = self._get_conn()
        rows = conn.execute("SELECT * FROM sandboxes").fetchall()
        conn.close()
        result: List[Sandbox] = [
            Sandbox(
                id=row["id"],
                name=row["name"],
                driver=row["driver"],
                status=row["status"],
                config=row["config"],
                created_at=row["created_at"],
            )
            for row in rows
        ]
        # sync cache
        self._sandboxes = {s.id: s for s in result}
        return result

    def _sync_cache(self) -> None:
        """Rebuild in-memory cache from DB — call after bulk operations."""
        conn = self._get_conn()
        rows = conn.execute("SELECT * FROM sandboxes").fetchall()
        conn.close()
        self._sandboxes = {
            row["id"]: Sandbox(
                id=row["id"],
                name=row["name"],
                driver=row["driver"],
                status=row["status"],
                config=row["config"],
                created_at=row["created_at"],
            )
            for row in rows
        }
