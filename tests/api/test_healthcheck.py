import pytest
from httpx import AsyncClient
from api.app.main import app

@pytest.mark.asyncio
async def test_healthcheck():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

