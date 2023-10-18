import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from fastapi_mctools.middlewares.trustedhost import TrustedHostMiddleware

app = FastAPI()
app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["example.com"], first_two_vpc_ip="10.0"
)


@app.get("/")
async def read_root():
    return {"message": "hello world"}


@pytest.mark.asyncio
async def test_trusted_host_middleware():
    async with AsyncClient(app=app, base_url="http://example.com") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "hello world"}

    # VPC IP 시작이 10.0인 경우를 테스트
    async with AsyncClient(app=app, base_url="http://10.0.0.1") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "hello world"}

    # 허용되지 않은 호스트를 테스트
    async with AsyncClient(app=app, base_url="http://notallowed.com") as ac:
        response = await ac.get("/")
    assert response.status_code != 200
