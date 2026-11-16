import pytest
from httpx import AsyncClient, ASGITransport
from app.main import create_app


@pytest.fixture
async def client():
    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_create_sandbox(client: AsyncClient):
    response = await client.post("/api/v1/sandboxes", json={})
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["status"] == "created"


@pytest.mark.asyncio
async def test_start_sandbox(client: AsyncClient):
    # First create a sandbox
    create_resp = await client.post("/api/v1/sandboxes", json={})
    assert create_resp.status_code == 200
    create_data = create_resp.json()
    sandbox_id = create_data["id"]

    # Start it
    start_resp = await client.post(f"/api/v1/sandboxes/{sandbox_id}/start")
    assert start_resp.status_code == 200
    start_data = start_resp.json()
    assert start_data["status"] == "running"


@pytest.mark.asyncio
async def test_stop_sandbox(client: AsyncClient):
    # Create and start first
    create_resp = await client.post("/api/v1/sandboxes", json={})
    sandbox_id = create_resp.json()["id"]
    await client.post(f"/api/v1/sandboxes/{sandbox_id}/start")

    stop_resp = await client.post(f"/api/v1/sandboxes/{sandbox_id}/stop")
    assert stop_resp.status_code == 200
    stop_data = stop_resp.json()
    assert stop_data["status"] == "stopped"


@pytest.mark.asyncio
async def test_destroy_sandbox(client: AsyncClient):
    # Create a sandbox
    create_resp = await client.post("/api/v1/sandboxes", json={})
    sandbox_id = create_resp.json()["id"]

    destroy_resp = await client.delete(f"/api/v1/sandboxes/{sandbox_id}")
    assert destroy_resp.status_code == 200
    destroy_data = destroy_resp.json()
    assert destroy_data["status"] == "destroyed"

    # Ensure it's gone (optional)
    get_resp = await client.get(f"/api/v1/sandboxes/{sandbox_id}")
    # Since we don't have a get endpoint, we skip
