import pytest
from httpx import ASGITransport, AsyncClient

from app.tests.test_database import get_test_db
from app.main import app
from app.deps.dependencies import get_db


app.dependency_overrides[get_db] = get_test_db


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_get_data_point():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        login_response = await ac.post(
            "/auth/login",
            data={"username": "admin", "password": "admin"},
        )
    assert login_response.status_code == 200, login_response.text
    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        get_response = await ac.get("/api/data", headers=headers)
    assert get_response.status_code == 200, get_response.text
