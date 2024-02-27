import pytest
from fastapi_mctools.utils.requests import APIClient
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


@pytest.fixture
async def api_client():
    api_client = APIClient()
    await api_client.start()
    yield api_client
    await api_client.close()


async def test_start(api_client: APIClient):
    assert isinstance(api_client.session, AsyncClient)


async def test_get(api_client: APIClient):
    response = await api_client.get("https://httpbin.org/get")
    assert response.status_code == 200


async def test_post(api_client: APIClient):
    response = await api_client.post("https://httpbin.org/post", json={"key": "value"})
    assert response.status_code == 200


async def test_put(api_client: APIClient):
    response = await api_client.put("https://httpbin.org/put", json={"key": "value"})
    assert response.status_code == 200


async def test_patch(api_client: APIClient):
    response = await api_client.patch("https://httpbin.org/patch", json={"key": "value"})
    assert response.status_code == 200
