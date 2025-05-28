import pytest
from httpx import AsyncClient
from api.app.main import app

@pytest.mark.asyncio
async def test_predict_valid_input():
    payload = {
        "features": [1.2, 3.4, 5.6]  # adapte conforme esperado
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/predict", json=payload)
    assert response.status_code == 200
    assert "prediction" in response.json()

